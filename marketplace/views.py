from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST, require_http_methods

from .forms import (
    BidForm,
    BidStatusForm,
    FinalizationContactForm,
    FinalizationPaymentForm,
    ProfileForm,
    RegisterForm,
)
from .models import Artwork, Bid, BidFinalization, Favorite, Profile, Seller

FINALIZATION_STEPS = ['contact', 'payment', 'review', 'confirmation']
FINALIZATION_SESSION_PREFIX = 'finalization_bid_'
DEMO_USERNAME = 'demo_collector'


def demo_user():
    User = get_user_model()
    demo = User.objects.filter(username=DEMO_USERNAME).first()
    if demo:
        return demo

    bidder_id = Bid.objects.order_by('-created_at').values_list('bidder_id', flat=True).first()
    if bidder_id:
        return User.objects.filter(pk=bidder_id).first()

    return User.objects.first()


def acting_user(request):
    if request.user.is_authenticated:
        return request.user
    return demo_user()


def get_or_create_profile(user):
    return Profile.objects.get_or_create(
        user=user,
        defaults={'name': user.get_full_name() or user.get_username()},
    )[0]


def artwork_queryset():
    return (
        Artwork.objects.select_related('seller', 'seller__user')
        .prefetch_related('images', 'bids')
        .annotate(
            accepted_bid_count=Count(
                'bids',
                filter=Q(bids__status=Bid.BidStatus.ACCEPTED),
            )
        )
    )


def favorite_artwork_ids(user):
    if not user.is_authenticated:
        return []
    return list(
        Favorite.objects.filter(user=user).values_list('artwork_id', flat=True)
    )


def redirect_after_toggle(request, fallback):
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(next_url)
    return redirect(fallback)


def current_seller(user):
    try:
        return user.seller
    except (AttributeError, Seller.DoesNotExist):
        return None


def home(request):
    active_finalization = active_finalization_redirect(request)
    if active_finalization:
        return active_finalization

    latest_artworks = artwork_queryset().order_by('-created_at')[:4]
    return render(
        request,
        'marketplace/home.html',
        {
            'latest_artworks': latest_artworks,
            'favorite_artwork_ids': favorite_artwork_ids(request.user),
        },
    )


def artwork_list(request):
    artworks = artwork_queryset()
    query = request.GET.get('q', '').strip()
    medium = request.GET.get('medium', '').strip()
    style = request.GET.get('style', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    order = request.GET.get('order', '').strip()

    if query:
        artworks = artworks.filter(title__icontains=query)
    if medium:
        artworks = artworks.filter(medium__iexact=medium)
    if style:
        artworks = artworks.filter(style__iexact=style)
    if min_price:
        try:
            artworks = artworks.filter(price__gte=Decimal(min_price))
        except InvalidOperation:
            messages.error(request, 'Minimum price must be a valid number.')
    if max_price:
        try:
            artworks = artworks.filter(price__lte=Decimal(max_price))
        except InvalidOperation:
            messages.error(request, 'Maximum price must be a valid number.')

    order_options = {
        'price': 'price',
        '-price': '-price',
        'title': 'title',
        '-title': '-title',
    }
    if order in order_options:
        artworks = artworks.order_by(order_options[order])
    else:
        artworks = artworks.order_by('-created_at')

    paginator = Paginator(artworks, 48)
    page_obj = paginator.get_page(request.GET.get('page'))
    mediums = Artwork.objects.order_by('medium').values_list('medium', flat=True).distinct()
    styles = Artwork.objects.order_by('style').values_list('style', flat=True).distinct()

    return render(
        request,
        'marketplace/artwork_list.html',
        {
            'page_obj': page_obj,
            'mediums': mediums,
            'styles': styles,
            'filters': {
                'q': query,
                'medium': medium,
                'style': style,
                'min_price': min_price,
                'max_price': max_price,
                'order': order,
            },
            'favorite_artwork_ids': favorite_artwork_ids(request.user),
        },
    )


def artwork_detail(request, pk):
    artwork = get_object_or_404(artwork_queryset(), pk=pk)
    existing_bid = None
    user = acting_user(request)
    if user:
        existing_bid = Bid.objects.filter(artwork=artwork, bidder=user).first()

    return render(
        request,
        'marketplace/artwork_detail.html',
        {
            'artwork': artwork,
            'existing_bid': existing_bid,
            'form': BidForm(instance=existing_bid),
            'is_favorite': (
                user is not None and Favorite.objects.filter(artwork=artwork, user=user).exists()
            ),
        },
    )


def seller_detail(request, pk):
    seller = get_object_or_404(
        Seller.objects.select_related('user').prefetch_related('artworks__images'),
        pk=pk,
    )
    artworks = seller.artworks.annotate(
        accepted_bid_count=Count(
            'bids',
            filter=Q(bids__status=Bid.BidStatus.ACCEPTED),
        )
    )
    return render(
        request,
        'marketplace/seller_detail.html',
        {'seller': seller, 'artworks': artworks},
    )


def register(request):
    if request.user.is_authenticated:
        return redirect('marketplace:home')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Your account was created successfully.')
        return redirect('marketplace:home')

    return render(request, 'marketplace/register.html', {'form': form})


def profile(request):
    user = acting_user(request)
    if user is None:
        form = ProfileForm(request.POST or None)
        return render(request, 'marketplace/profile.html', {'form': form})

    user_profile = Profile.objects.filter(user=user).first()
    if request.method == 'POST' and user_profile is None:
        user_profile = get_or_create_profile(user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=user_profile)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('marketplace:profile')
        messages.error(request, 'Profile update failed. Please check the fields below.')

    return render(request, 'marketplace/profile.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def submit_bid(request, pk):
    artwork = get_object_or_404(artwork_queryset(), pk=pk)
    user = acting_user(request)
    if user is None:
        messages.error(request, 'Demo bidding is not available until sample users are loaded.')
        return redirect('marketplace:artwork_detail', pk=artwork.pk)

    if artwork.is_sold:
        messages.error(request, 'This artwork has already been sold.')
        return redirect('marketplace:artwork_detail', pk=artwork.pk)
    if current_seller(user) == artwork.seller:
        messages.error(request, 'Sellers cannot bid on their own artwork.')
        return redirect('marketplace:artwork_detail', pk=artwork.pk)

    existing_bid = Bid.objects.filter(artwork=artwork, bidder=user).first()
    form = BidForm(request.POST if request.method == 'POST' else None, instance=existing_bid)

    if request.method == 'POST':
        if form.is_valid():
            bid = form.save(commit=False)
            bid.artwork = artwork
            bid.bidder = user
            bid.status = Bid.BidStatus.PENDING
            bid.save()
            messages.success(request, 'Your bid was submitted successfully.')
            return redirect('marketplace:artwork_detail', pk=artwork.pk)
        messages.error(request, 'Bid submission failed. Please check the fields below.')

    return render(
        request,
        'marketplace/bid_form.html',
        {
            'artwork': artwork,
            'form': form,
            'existing_bid': existing_bid,
        },
    )


def bid_list(request):
    bids = Bid.objects.select_related(
        'artwork',
        'artwork__seller',
        'artwork__seller__user',
    ).order_by('-created_at')
    if request.user.is_authenticated:
        bids = bids.filter(bidder=request.user)
    return render(request, 'marketplace/bid_list.html', {'bids': bids})


@login_required
def seller_bid_list(request):
    seller = current_seller(request.user)
    bids = Bid.objects.none()
    if seller is None:
        messages.error(request, 'Only seller accounts can manage artwork bids.')
    else:
        bids = (
            Bid.objects.filter(artwork__seller=seller)
            .select_related('artwork', 'bidder', 'bidder__profile')
            .order_by('-created_at')
        )

    return render(
        request,
        'marketplace/seller_bid_list.html',
        {
            'seller': seller,
            'bids': bids,
            'bid_status_choices': Bid.BidStatus.choices,
        },
    )


@login_required
@require_POST
def update_seller_bid_status(request, pk):
    bid = get_object_or_404(
        Bid.objects.select_related('artwork', 'artwork__seller'),
        pk=pk,
        artwork__seller__user=request.user,
    )
    if hasattr(bid, 'finalization') and bid.finalization.finalized_at:
        messages.error(request, 'Finalized bids can no longer be changed.')
        return redirect_after_toggle(request, 'marketplace:seller_bid_list')

    form = BidStatusForm(request.POST, instance=bid)
    if form.is_valid():
        new_status = form.cleaned_data['status']
        if (
            new_status == Bid.BidStatus.ACCEPTED
            and Bid.objects.filter(
                artwork=bid.artwork,
                status=Bid.BidStatus.ACCEPTED,
            ).exclude(pk=bid.pk).exists()
        ):
            messages.error(request, 'This artwork already has an accepted bid.')
            return redirect_after_toggle(request, 'marketplace:seller_bid_list')

        with transaction.atomic():
            bid = form.save()
            if bid.status == Bid.BidStatus.ACCEPTED:
                Bid.objects.filter(artwork=bid.artwork).exclude(pk=bid.pk).update(
                    status=Bid.BidStatus.REJECTED,
                )
        messages.success(request, f'Bid for {bid.artwork.title} was marked {bid.status}.')
    else:
        messages.error(request, 'Bid status could not be updated.')

    return redirect_after_toggle(request, 'marketplace:seller_bid_list')


def favorite_list(request):
    user = acting_user(request)
    if user is None:
        return render(
            request,
            'marketplace/favorite_list.html',
            {
                'artworks': [],
                'favorite_artwork_ids': [],
            },
        )

    favorites = (
        Favorite.objects.filter(user=user)
        .select_related('artwork', 'artwork__seller', 'artwork__seller__user')
        .prefetch_related('artwork__images')
    )
    artworks = [favorite.artwork for favorite in favorites]
    return render(
        request,
        'marketplace/favorite_list.html',
        {
            'artworks': artworks,
            'favorite_artwork_ids': [artwork.pk for artwork in artworks],
        },
    )


@require_POST
def toggle_favorite(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    user = acting_user(request)
    if user is None:
        messages.error(request, 'Demo favorites are not available until sample users are loaded.')
        return redirect_after_toggle(request, 'marketplace:artwork_list')

    favorite, created = Favorite.objects.get_or_create(
        artwork=artwork,
        user=user,
    )
    if created:
        messages.success(request, f'{artwork.title} was added to your favorites.')
    else:
        favorite.delete()
        messages.success(request, f'{artwork.title} was removed from your favorites.')
    return redirect_after_toggle(request, 'marketplace:artwork_list')


def finalization_session_key(bid):
    return f'{FINALIZATION_SESSION_PREFIX}{bid.pk}'


def get_finalization_data(request, bid):
    return request.session.get(finalization_session_key(bid), {})


def save_finalization_data(request, bid, data):
    request.session[finalization_session_key(bid)] = data
    request.session.modified = True


def finalization_context(bid, step, data, **extra):
    context = {
        'bid': bid,
        'current_step': step,
        'finalization_locked': step != 'confirmation',
        'has_contact': 'contact' in data,
        'has_payment': 'payment' in data,
    }
    context.update(extra)
    return context


def next_finalization_step(data):
    if 'payment' in data:
        return 'review'
    if 'contact' in data:
        return 'payment'
    return 'contact'


def active_finalization_redirect(request):
    if not request.user.is_authenticated:
        return None

    for key, data in request.session.items():
        if not key.startswith(FINALIZATION_SESSION_PREFIX):
            continue
        try:
            bid_pk = int(key.removeprefix(FINALIZATION_SESSION_PREFIX))
        except ValueError:
            continue

        bid = (
            Bid.objects.filter(
                pk=bid_pk,
                bidder=request.user,
                status__in=[Bid.BidStatus.ACCEPTED, Bid.BidStatus.CONTINGENT],
            )
            .select_related('finalization')
            .first()
        )
        if not bid:
            continue
        if hasattr(bid, 'finalization') and bid.finalization.finalized_at:
            continue

        return redirect(
            'marketplace:finalize_bid_step',
            pk=bid.pk,
            step=next_finalization_step(data),
        )

    return None


@require_http_methods(['GET', 'POST'])
def finalize_bid(request, pk, step='contact'):
    bids = Bid.objects.select_related('artwork', 'artwork__seller')
    if request.user.is_authenticated:
        bids = bids.filter(bidder=request.user)
    bid = get_object_or_404(bids, pk=pk)
    if bid.status not in [Bid.BidStatus.ACCEPTED, Bid.BidStatus.CONTINGENT]:
        messages.error(request, 'Only accepted or contingent bids can be finalized.')
        return redirect('marketplace:bid_list')

    is_finalized = hasattr(bid, 'finalization') and bid.finalization.finalized_at
    if is_finalized and step != 'confirmation':
        return redirect('marketplace:finalize_bid_step', pk=bid.pk, step='confirmation')

    if step not in FINALIZATION_STEPS:
        return redirect('marketplace:finalize_bid_step', pk=bid.pk, step='contact')

    data = get_finalization_data(request, bid)

    if step == 'confirmation':
        if is_finalized or data.get('confirmed'):
            return render(
                request,
                'marketplace/finalize_confirmation.html',
                finalization_context(bid, step, data),
            )
        messages.error(request, 'Please review and confirm the bid before viewing confirmation.')
        if 'payment' in data:
            return redirect('marketplace:finalize_bid_step', pk=bid.pk, step='review')
        if 'contact' in data:
            return redirect('marketplace:finalize_bid_step', pk=bid.pk, step='payment')
        return redirect('marketplace:finalize_bid_step', pk=bid.pk, step='contact')

    if step == 'contact':
        form = FinalizationContactForm(
            request.POST if request.method == 'POST' else None,
            initial=data.get('contact'),
        )
        if request.method == 'POST' and form.is_valid():
            data['contact'] = form.cleaned_data
            save_finalization_data(request, bid, data)
            return redirect('marketplace:finalize_bid_step', pk=bid.pk, step='payment')
        return render(
            request,
            'marketplace/finalize_contact.html',
            finalization_context(bid, step, data, form=form),
        )

    if step == 'payment':
        if 'contact' not in data:
            return redirect('marketplace:finalize_bid_step', pk=bid.pk, step='contact')
        form = FinalizationPaymentForm(
            request.POST if request.method == 'POST' else None,
            initial=data.get('payment'),
        )
        if request.method == 'POST' and form.is_valid():
            data['payment'] = form.cleaned_data
            save_finalization_data(request, bid, data)
            return redirect('marketplace:finalize_bid_step', pk=bid.pk, step='review')
        return render(
            request,
            'marketplace/finalize_payment.html',
            finalization_context(bid, step, data, form=form),
        )

    if step == 'review':
        if 'contact' not in data:
            return redirect('marketplace:finalize_bid_step', pk=bid.pk, step='contact')
        if 'payment' not in data:
            return redirect('marketplace:finalize_bid_step', pk=bid.pk, step='payment')
        if request.method == 'POST':
            contact = data['contact']
            payment = data['payment']
            if request.user.is_authenticated:
                address = (
                    f"{contact['street_name']}, {contact['city']} "
                    f"{contact['postal_code']}, {contact['country']}"
                )
                finalization, _ = BidFinalization.objects.update_or_create(
                    bid=bid,
                    defaults={
                        'address': address,
                        'street_name': contact['street_name'],
                        'city': contact['city'],
                        'postal_code': contact['postal_code'],
                        'country': contact['country'],
                        'national_id': contact['national_id'],
                        'payment_method': payment['payment_method'],
                        'payment_info': payment['payment_method'].replace('_', ' ').title(),
                        'cardholder_name': payment.get('cardholder_name', ''),
                        'credit_card_number': payment.get('credit_card_number', ''),
                        'expiry_date': payment.get('expiry_date', ''),
                        'cvc': payment.get('cvc', ''),
                        'bank_account': payment.get('bank_account', ''),
                        'sending_bank': payment.get('sending_bank', ''),
                        'routing_number': payment.get('routing_number', ''),
                        'account_number': payment.get('account_number', ''),
                    },
                )
                finalization.mark_finalized()
                request.session.pop(finalization_session_key(bid), None)
            else:
                data['confirmed'] = True
                save_finalization_data(request, bid, data)
            messages.success(request, 'Your bid was finalized successfully.')
            return redirect('marketplace:finalize_bid_step', pk=bid.pk, step='confirmation')

        return render(
            request,
            'marketplace/finalize_review.html',
            finalization_context(
                bid,
                step,
                data,
                contact=data['contact'],
                payment=data['payment'],
                payment_method_label=dict(FinalizationPaymentForm.PAYMENT_CHOICES)[
                    data['payment']['payment_method']
                ],
            ),
        )
