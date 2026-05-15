from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Seller(models.Model):
    class SellerType(models.TextChoices):
        INDIVIDUAL = 'Individual', 'Individual'
        GALLERY = 'Gallery', 'Gallery'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=255, blank=True)
    seller_type = models.CharField(max_length=20, choices=SellerType.choices)
    address = models.TextField()
    street_name = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120, blank=True)
    postal_code = models.CharField(max_length=30, blank=True)
    logo = models.ImageField(
        upload_to='seller_logos/',
        blank=True,
        null=True,
    )
    cover = models.ImageField(
        upload_to='seller_covers/',
        blank=True,
        null=True,
    )
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.seller_type})'

    @property
    def name(self):
        if self.display_name:
            return self.display_name
        profile = getattr(self.user, 'profile', None)
        if profile and profile.name:
            return profile.name
        return self.user.get_username()

    @property
    def gallery_address(self):
        address_parts = [self.street_name, self.city, self.postal_code]
        clean_parts = [part for part in address_parts if part]
        return ', '.join(clean_parts) or self.address


class Artwork(models.Model):
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name='artworks',
    )
    title = models.CharField(max_length=255)
    medium = models.CharField(max_length=120)
    style = models.CharField(max_length=120)
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    dimensions = models.CharField(max_length=120)
    year = models.PositiveIntegerField()
    edition = models.CharField(max_length=120, blank=True)
    provenance = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def starting_bid_price(self):
        return self.price

    @property
    def listing_date(self):
        return self.created_at

    @property
    def is_sold(self):
        accepted_bid_count = getattr(self, 'accepted_bid_count', None)
        if accepted_bid_count is not None:
            return accepted_bid_count > 0
        return self.bids.filter(status=Bid.BidStatus.ACCEPTED).exists()

    @property
    def thumbnail(self):
        return self.images.first()


class ArtworkImage(models.Model):
    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(upload_to='artwork_images/')
    alt_text = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        return f'Image for {self.artwork}'


class Bid(models.Model):
    class BidStatus(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        ACCEPTED = 'Accepted', 'Accepted'
        REJECTED = 'Rejected', 'Rejected'
        CONTINGENT = 'Contingent', 'Contingent'

    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.CASCADE,
        related_name='bids',
    )
    bidder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bids',
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    expiration = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=BidStatus.choices,
        default=BidStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['artwork', 'bidder'],
                name='unique_bid_per_artwork_and_bidder',
            )
        ]

    def __str__(self):
        return f'{self.bidder} bid {self.price} on {self.artwork}'


class BidFinalization(models.Model):
    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = 'credit_card', 'Credit card'
        BANK_TRANSFER = 'bank_transfer', 'Bank transfer'
        WIRE_TRANSFER = 'wire_transfer', 'Wire transfer'

    bid = models.OneToOneField(
        Bid,
        on_delete=models.CASCADE,
        related_name='finalization',
    )
    address = models.TextField()
    street_name = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120, blank=True)
    postal_code = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=120, blank=True)
    national_id = models.CharField(max_length=30, blank=True)
    payment_method = models.CharField(
        max_length=30,
        choices=PaymentMethod.choices,
        blank=True,
    )
    payment_info = models.CharField(
        max_length=255,
        help_text='Store only non-sensitive payment references or summaries.',
    )
    cardholder_name = models.CharField(max_length=255, blank=True)
    credit_card_number = models.CharField(max_length=30, blank=True)
    expiry_date = models.CharField(max_length=10, blank=True)
    cvc = models.CharField(max_length=10, blank=True)
    bank_account = models.CharField(max_length=80, blank=True)
    sending_bank = models.CharField(max_length=255, blank=True)
    routing_number = models.CharField(max_length=80, blank=True)
    account_number = models.CharField(max_length=80, blank=True)
    finalized_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Finalization for {self.bid}'

    def mark_finalized(self):
        self.finalized_at = timezone.now()
        self.save(update_fields=['finalized_at', 'updated_at'])
