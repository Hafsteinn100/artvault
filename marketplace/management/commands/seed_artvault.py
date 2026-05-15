from datetime import timedelta
from pathlib import Path
import shutil

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from marketplace.models import Artwork, ArtworkImage, Bid, BidFinalization, Profile, Seller


DEMO_PASSWORD = 'artvault123'

BUYERS = [
    {
        'username': 'collector',
        'email': 'collector@example.com',
        'name': 'Marta Collector',
        'profile_image': 'profile.png',
    },
    {
        'username': 'anna_buyer',
        'email': 'anna.buyer@example.com',
        'name': 'Anna Jonsdottir',
        'profile_image': 'profile.png',
    },
    {
        'username': 'marco_collector',
        'email': 'marco.collector@example.com',
        'name': 'Marco Rossi',
        'profile_image': 'profile.png',
    },
]

SELLERS = [
    {
        'username': 'elena_artist',
        'email': 'elena.varga@example.com',
        'name': 'Elena Varga',
        'display_name': 'Elena Varga',
        'seller_type': Seller.SellerType.INDIVIDUAL,
        'street_name': '',
        'city': '',
        'postal_code': '',
        'logo': 'profile.png',
        'cover': 'medium-oil.jpg',
        'bio': 'Contemporary abstract painter working from a small Reykjavik studio.',
    },
    {
        'username': 'studio_kaito',
        'email': 'studio.kaito@example.com',
        'name': 'Studio Kaito',
        'display_name': 'Studio Kaito',
        'seller_type': Seller.SellerType.INDIVIDUAL,
        'street_name': '',
        'city': '',
        'postal_code': '',
        'logo': 'profile.png',
        'cover': 'pexels-ricky-kwong-113005840-35589498.jpg',
        'bio': 'Photographer documenting city weather, glass, and late-night streets.',
    },
    {
        'username': 'nordic_gallery',
        'email': 'gallery@example.com',
        'name': 'Nordic Light Gallery',
        'display_name': 'Nordic Light Gallery',
        'seller_type': Seller.SellerType.GALLERY,
        'street_name': 'Laugavegur 24',
        'city': 'Reykjavik',
        'postal_code': '101',
        'logo': 'profile.png',
        'cover': 'coverimg2verklegt2.webp',
        'bio': 'A curated gallery focused on Nordic modern art and emerging artists.',
    },
    {
        'username': 'aurora_fine_arts',
        'email': 'aurora@example.com',
        'name': 'Aurora Fine Arts',
        'display_name': 'Aurora Fine Arts',
        'seller_type': Seller.SellerType.GALLERY,
        'street_name': 'Austurstraeti 12',
        'city': 'Reykjavik',
        'postal_code': '101',
        'logo': 'profile.png',
        'cover': 'pexels-sarmat-batagov-776392502-35072454.jpg',
        'bio': 'Gallery specializing in sculpture, realism, and high-value private sales.',
    },
]

ARTWORKS = [
    {
        'title': 'Midnight Fjord',
        'seller': 'elena_artist',
        'medium': 'Oil',
        'style': 'Impressionism',
        'price': '120000.00',
        'dimensions': '80 x 60 cm',
        'year': 2024,
        'edition': 'Original',
        'provenance': 'Acquired directly from the artist after a private studio showing.',
        'images': ['oilpaint1.jpeg', 'medium-oil.jpg'],
        'listed_days_ago': 2,
    },
    {
        'title': 'Red Horizon',
        'seller': 'elena_artist',
        'medium': 'Watercolour',
        'style': 'Abstract',
        'price': '45000.00',
        'dimensions': '40 x 30 cm',
        'year': 2023,
        'edition': 'Limited edition',
        'provenance': 'Part of a small colour-study series retained by the artist.',
        'images': ['medium-watercolor.jpg', 'digitalart1.jpeg'],
        'listed_days_ago': 4,
    },
    {
        'title': 'Harbor Morning',
        'seller': 'elena_artist',
        'medium': 'Watercolour',
        'style': 'Realism',
        'price': '55000.00',
        'dimensions': '35 x 25 cm',
        'year': 2022,
        'edition': 'Original',
        'provenance': 'Painted on location and kept in the artist archive until listing.',
        'images': ['medium-watercolor.jpg', 'pexels-minan1398-813269.jpg'],
        'listed_days_ago': 6,
    },
    {
        'title': 'Soft Meridian',
        'seller': 'elena_artist',
        'medium': 'Oil',
        'style': 'Modern',
        'price': '87000.00',
        'dimensions': '65 x 50 cm',
        'year': 2025,
        'edition': 'Original',
        'provenance': 'First shown during an independent Reykjavik studio weekend.',
        'images': ['medium-oil.jpg', 'oilpaint1.jpeg'],
        'listed_days_ago': 8,
    },
    {
        'title': 'City Rain',
        'seller': 'studio_kaito',
        'medium': 'Photography',
        'style': 'Realism',
        'price': '75000.00',
        'dimensions': '50 x 70 cm',
        'year': 2024,
        'edition': 'Limited edition',
        'provenance': 'Printed from the artist-owned digital negative.',
        'images': ['pexels-ricky-kwong-113005840-35589498.jpg', 'medium-photography.jpg'],
        'listed_days_ago': 3,
    },
    {
        'title': 'Urban Collection',
        'seller': 'studio_kaito',
        'medium': 'Photography',
        'style': 'Modern',
        'price': '87000.00',
        'dimensions': '60 x 40 cm',
        'year': 2023,
        'edition': 'Open edition',
        'provenance': 'Released as part of the artist city-light portfolio.',
        'images': ['medium-photography.jpg', 'pexels-ricky-kwong-113005840-35589498.jpg'],
        'listed_days_ago': 10,
    },
    {
        'title': 'Green Gallery Study',
        'seller': 'studio_kaito',
        'medium': 'Photography',
        'style': 'Impressionism',
        'price': '62000.00',
        'dimensions': '45 x 60 cm',
        'year': 2021,
        'edition': 'Limited edition',
        'provenance': 'Previously held in a small private collection.',
        'images': ['pexels-minan1398-813269.jpg', 'medium-photography.jpg'],
        'listed_days_ago': 12,
    },
    {
        'title': 'Concrete Light',
        'seller': 'studio_kaito',
        'medium': 'Photography',
        'style': 'Abstract',
        'price': '39000.00',
        'dimensions': '30 x 45 cm',
        'year': 2025,
        'edition': 'Open edition',
        'provenance': 'Created for ArtVault as an accessible collector print.',
        'images': ['medium-photography.jpg', 'digitalart1.jpeg'],
        'listed_days_ago': 14,
    },
    {
        'title': 'Northern Light Study',
        'seller': 'nordic_gallery',
        'medium': 'Oil',
        'style': 'Modern',
        'price': '160000.00',
        'dimensions': '90 x 70 cm',
        'year': 2020,
        'edition': 'Original',
        'provenance': 'Consigned by the first buyer after a 2021 gallery exhibition.',
        'images': ['coverimg2verklegt2.webp', 'medium-oil.jpg'],
        'listed_days_ago': 5,
    },
    {
        'title': 'Glass Memory',
        'seller': 'nordic_gallery',
        'medium': 'Sculpture',
        'style': 'Abstract',
        'price': '220000.00',
        'dimensions': '45 x 45 x 35 cm',
        'year': 2019,
        'edition': 'Original',
        'provenance': 'Held by Nordic Light Gallery since its 2019 sculpture program.',
        'images': ['medium-sculpture.jpg', 'coverimg2verklegt2.webp'],
        'listed_days_ago': 7,
    },
    {
        'title': 'Blue Geometry',
        'seller': 'nordic_gallery',
        'medium': 'Oil',
        'style': 'Abstract',
        'price': '98000.00',
        'dimensions': '60 x 60 cm',
        'year': 2022,
        'edition': 'Limited edition',
        'provenance': 'Returned from a corporate collection refresh.',
        'images': ['medium-oil.jpg', 'digitalart1.jpeg'],
        'listed_days_ago': 9,
    },
    {
        'title': 'Winter Cabinet',
        'seller': 'nordic_gallery',
        'medium': 'Watercolour',
        'style': 'Realism',
        'price': '68000.00',
        'dimensions': '42 x 30 cm',
        'year': 2018,
        'edition': 'Original',
        'provenance': 'Purchased directly from the artist estate.',
        'images': ['medium-watercolor.jpg', 'coverimg2verklegt2.webp'],
        'listed_days_ago': 16,
    },
    {
        'title': 'Silent Form',
        'seller': 'aurora_fine_arts',
        'medium': 'Sculpture',
        'style': 'Modern',
        'price': '300000.00',
        'dimensions': '35 x 70 x 28 cm',
        'year': 2021,
        'edition': 'Original',
        'provenance': 'Previously shown in a private sculpture salon.',
        'images': ['medium-sculpture.jpg', 'pexels-sarmat-batagov-776392502-35072454.jpg'],
        'listed_days_ago': 1,
    },
    {
        'title': 'Marble Echo',
        'seller': 'aurora_fine_arts',
        'medium': 'Sculpture',
        'style': 'Realism',
        'price': '280000.00',
        'dimensions': '30 x 65 x 30 cm',
        'year': 2017,
        'edition': 'Original',
        'provenance': 'Acquired from a European private collection.',
        'images': ['medium-sculpture.jpg', 'pexels-sarmat-batagov-776392502-35072454.jpg'],
        'listed_days_ago': 11,
    },
    {
        'title': 'White Signal',
        'seller': 'aurora_fine_arts',
        'medium': 'Sculpture',
        'style': 'Impressionism',
        'price': '205000.00',
        'dimensions': '28 x 48 x 24 cm',
        'year': 2020,
        'edition': 'Limited edition',
        'provenance': 'One of six cast works from the artist workshop.',
        'images': ['medium-sculpture.jpg', 'medium-digital.jpg'],
        'listed_days_ago': 13,
    },
    {
        'title': 'Field Archive',
        'seller': 'aurora_fine_arts',
        'medium': 'Watercolour',
        'style': 'Modern',
        'price': '112000.00',
        'dimensions': '75 x 55 cm',
        'year': 2025,
        'edition': 'Original',
        'provenance': 'Newly listed work from the gallery spring catalogue.',
        'images': ['medium-watercolor.jpg', 'medium-digital.jpg'],
        'listed_days_ago': 15,
    },
]

BIDS = [
    {
        'bidder': 'anna_buyer',
        'artwork': 'Midnight Fjord',
        'price': '130000.00',
        'status': Bid.BidStatus.PENDING,
        'expires_in_days': 10,
    },
    {
        'bidder': 'anna_buyer',
        'artwork': 'Silent Form',
        'price': '320000.00',
        'status': Bid.BidStatus.ACCEPTED,
        'expires_in_days': 20,
    },
    {
        'bidder': 'anna_buyer',
        'artwork': 'City Rain',
        'price': '80000.00',
        'status': Bid.BidStatus.REJECTED,
        'expires_in_days': 8,
    },
    {
        'bidder': 'anna_buyer',
        'artwork': 'Glass Memory',
        'price': '240000.00',
        'status': Bid.BidStatus.CONTINGENT,
        'expires_in_days': 14,
    },
    {
        'bidder': 'marco_collector',
        'artwork': 'Northern Light Study',
        'price': '170000.00',
        'status': Bid.BidStatus.ACCEPTED,
        'expires_in_days': 18,
    },
    {
        'bidder': 'marco_collector',
        'artwork': 'Harbor Morning',
        'price': '58000.00',
        'status': Bid.BidStatus.PENDING,
        'expires_in_days': 12,
    },
    {
        'bidder': 'marco_collector',
        'artwork': 'Marble Echo',
        'price': '290000.00',
        'status': Bid.BidStatus.REJECTED,
        'expires_in_days': 9,
    },
    {
        'bidder': 'collector',
        'artwork': 'Blue Geometry',
        'price': '105000.00',
        'status': Bid.BidStatus.CONTINGENT,
        'expires_in_days': 16,
    },
]

FINALIZATIONS = [
    {
        'bidder': 'anna_buyer',
        'artwork': 'Silent Form',
        'contact': {
            'street_name': 'Hverfisgata 12',
            'city': 'Reykjavik',
            'postal_code': '101',
            'country': 'Iceland',
            'national_id': '010190-1234',
        },
        'payment': {
            'payment_method': BidFinalization.PaymentMethod.CREDIT_CARD,
            'payment_info': 'Credit Card ending 4242',
            'cardholder_name': 'Anna Jonsdottir',
            'credit_card_number': '4242 4242 4242 4242',
            'expiry_date': '12/28',
            'cvc': '123',
        },
    },
    {
        'bidder': 'marco_collector',
        'artwork': 'Northern Light Study',
        'contact': {
            'street_name': 'Bankastraeti 7',
            'city': 'Reykjavik',
            'postal_code': '101',
            'country': 'Iceland',
            'national_id': '020280-5679',
        },
        'payment': {
            'payment_method': BidFinalization.PaymentMethod.BANK_TRANSFER,
            'payment_info': 'Bank transfer from 0133-26-123456',
            'bank_account': '0133-26-123456',
        },
    },
]


class Command(BaseCommand):
    help = 'Seed the database with ArtVault demo users, sellers, artworks, images, and bids.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-demo',
            action='store_true',
            help="Delete this command's demo users and their related data before seeding.",
        )

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT)
        media_root.mkdir(parents=True, exist_ok=True)

        if options['clear_demo']:
            self.clear_demo_data()

        users = {}
        sellers = {}
        artworks = {}

        for buyer in BUYERS:
            users[buyer['username']] = self.create_user(
                buyer['username'],
                buyer['email'],
                buyer['name'],
                buyer['profile_image'],
            )

        for seller_data in SELLERS:
            user = self.create_user(
                seller_data['username'],
                seller_data['email'],
                seller_data['name'],
                seller_data['logo'],
            )
            users[seller_data['username']] = user
            sellers[seller_data['username']] = self.create_seller(user, seller_data)

        for artwork_data in ARTWORKS:
            artwork = self.create_artwork(sellers[artwork_data['seller']], artwork_data)
            artworks[artwork.title] = artwork

        bids = {}
        for bid_data in BIDS:
            bid = self.create_bid(
                artworks[bid_data['artwork']],
                users[bid_data['bidder']],
                bid_data,
            )
            bids[(bid_data['bidder'], bid_data['artwork'])] = bid

        for finalization_data in FINALIZATIONS:
            bid = bids[(finalization_data['bidder'], finalization_data['artwork'])]
            self.create_finalization(bid, finalization_data)

        self.stdout.write(self.style.SUCCESS('Seeded ArtVault demo data.'))
        self.stdout.write(f'Demo password for every seeded account: {DEMO_PASSWORD}')
        self.stdout.write('Buyer logins: collector, anna_buyer, marco_collector')
        self.stdout.write('Seller logins: elena_artist, studio_kaito, nordic_gallery, aurora_fine_arts')

    def clear_demo_data(self):
        demo_usernames = [user['username'] for user in BUYERS] + [
            seller['username'] for seller in SELLERS
        ]
        User.objects.filter(username__in=demo_usernames).delete()

    def create_user(self, username, email, name, profile_image):
        user, _ = User.objects.get_or_create(username=username)
        user.email = email
        user.first_name = name.split(' ', 1)[0]
        user.last_name = name.split(' ', 1)[1] if ' ' in name else ''
        user.set_password(DEMO_PASSWORD)
        user.save()

        Profile.objects.update_or_create(
            user=user,
            defaults={
                'name': name,
                'profile_image': self.copy_asset('profiles', profile_image),
            },
        )
        return user

    def create_seller(self, user, seller_data):
        address = ''
        if seller_data['seller_type'] == Seller.SellerType.GALLERY:
            address = (
                f"{seller_data['street_name']}, "
                f"{seller_data['city']} {seller_data['postal_code']}"
            )

        seller, _ = Seller.objects.update_or_create(
            user=user,
            defaults={
                'display_name': seller_data['display_name'],
                'seller_type': seller_data['seller_type'],
                'address': address,
                'street_name': seller_data['street_name'],
                'city': seller_data['city'],
                'postal_code': seller_data['postal_code'],
                'logo': self.copy_asset('seller_logos', seller_data['logo']),
                'cover': self.copy_asset('seller_covers', seller_data['cover']),
                'bio': seller_data['bio'],
            },
        )
        return seller

    def create_artwork(self, seller, artwork_data):
        artwork, _ = Artwork.objects.update_or_create(
            seller=seller,
            title=artwork_data['title'],
            defaults={
                'medium': artwork_data['medium'],
                'style': artwork_data['style'],
                'price': artwork_data['price'],
                'dimensions': artwork_data['dimensions'],
                'year': artwork_data['year'],
                'edition': artwork_data['edition'],
                'provenance': artwork_data['provenance'],
            },
        )
        listed_at = timezone.now() - timedelta(days=artwork_data['listed_days_ago'])
        Artwork.objects.filter(pk=artwork.pk).update(created_at=listed_at)
        artwork.refresh_from_db()

        ArtworkImage.objects.filter(artwork=artwork).delete()
        for index, image_name in enumerate(artwork_data['images']):
            ArtworkImage.objects.create(
                artwork=artwork,
                image=self.copy_asset('artwork_images', image_name),
                alt_text=f"{artwork.title} image {index + 1}",
                sort_order=index,
            )
        return artwork

    def create_bid(self, artwork, bidder, bid_data):
        bid, _ = Bid.objects.update_or_create(
            artwork=artwork,
            bidder=bidder,
            defaults={
                'price': bid_data['price'],
                'expiration': timezone.now() + timedelta(days=bid_data['expires_in_days']),
                'status': bid_data['status'],
            },
        )
        return bid

    def create_finalization(self, bid, finalization_data):
        contact = finalization_data['contact']
        payment = finalization_data['payment']
        address = (
            f"{contact['street_name']}, {contact['city']} "
            f"{contact['postal_code']}, {contact['country']}"
        )

        defaults = {
            'address': address,
            'street_name': contact['street_name'],
            'city': contact['city'],
            'postal_code': contact['postal_code'],
            'country': contact['country'],
            'national_id': contact['national_id'],
            'payment_method': payment['payment_method'],
            'payment_info': payment['payment_info'],
            'cardholder_name': payment.get('cardholder_name', ''),
            'credit_card_number': payment.get('credit_card_number', ''),
            'expiry_date': payment.get('expiry_date', ''),
            'cvc': payment.get('cvc', ''),
            'bank_account': payment.get('bank_account', ''),
            'sending_bank': payment.get('sending_bank', ''),
            'routing_number': payment.get('routing_number', ''),
            'account_number': payment.get('account_number', ''),
            'finalized_at': timezone.now(),
        }
        BidFinalization.objects.update_or_create(bid=bid, defaults=defaults)

    def copy_asset(self, folder, asset_name):
        source = self.find_asset_source(asset_name)
        destination_dir = Path(settings.MEDIA_ROOT) / folder
        destination_dir.mkdir(parents=True, exist_ok=True)
        destination = destination_dir / asset_name
        if source and source.exists() and not destination.exists():
            shutil.copyfile(source, destination)
        return f'{folder}/{asset_name}'

    def find_asset_source(self, asset_name):
        base_dir = Path(settings.BASE_DIR)
        candidates = [
            base_dir / asset_name,
            base_dir.parent / asset_name,
            base_dir / 'marketplace' / 'static' / 'marketplace' / asset_name,
        ]
        return next((candidate for candidate in candidates if candidate.exists()), None)
