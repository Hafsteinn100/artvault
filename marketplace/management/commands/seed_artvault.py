from datetime import timedelta
from pathlib import Path
import shutil

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from marketplace.models import Artwork, ArtworkImage, Bid, BidFinalization, Profile, Seller


class Command(BaseCommand):
    help = 'Seed the database with ArtVault demo users, sellers, artworks, images, and bids.'

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT)
        media_root.mkdir(parents=True, exist_ok=True)

        collector = self.create_user('collector', 'collector@example.com', 'Marta Collector')
        gallery_user = self.create_user('nordic_gallery', 'gallery@example.com', 'Nordic Gallery')
        artist_user = self.create_user('elias_artist', 'artist@example.com', 'Elias Stone')

        gallery = self.create_seller(
            gallery_user,
            display_name='Nordic Gallery',
            seller_type=Seller.SellerType.GALLERY,
            street_name='Austurstraeti 12',
            city='Reykjavik',
            postal_code='101',
            bio='A Reykjavik gallery focused on contemporary Nordic art.',
        )
        artist = self.create_seller(
            artist_user,
            display_name='Elias Stone',
            seller_type=Seller.SellerType.INDIVIDUAL,
            street_name='Hidden for individuals',
            city='Reykjavik',
            postal_code='105',
            bio='Independent artist working with light, texture, and layered surfaces.',
        )

        self.attach_media(gallery, 'logo', 'seller_logos', 'profile.png')
        self.attach_media(gallery, 'cover', 'seller_covers', 'coverimg2verklegt2.webp')
        self.attach_media(artist, 'logo', 'seller_logos', 'profile.png')
        self.attach_media(artist, 'cover', 'seller_covers', 'coverimg2verklegt2.webp')

        artworks = [
            self.create_artwork(
                gallery,
                'Bloom Study',
                'Oil',
                'Abstract',
                '1200.00',
                '80 x 60 cm',
                2024,
                'Original',
                'Acquired directly from the artist after a private studio showing.',
                ['medium-oil.jpg'],
            ),
            self.create_artwork(
                gallery,
                'Quiet Interior',
                'Watercolour',
                'Realism',
                '650.00',
                '42 x 30 cm',
                2023,
                'Limited edition',
                'Part of a small interior study collection.',
                ['medium-watercolor.jpg'],
            ),
            self.create_artwork(
                artist,
                'Spring Canopy',
                'Photography',
                'Modern',
                '900.00',
                '70 x 50 cm',
                2022,
                'Open edition',
                'Printed from the artist-owned digital negative.',
                ['medium-photography.jpg'],
            ),
            self.create_artwork(
                artist,
                'Prism Field',
                'Digital',
                'Modern',
                '480.00',
                '60 x 60 cm',
                2025,
                'Original',
                'Created as part of an experimental generative art series.',
                ['medium-digital.jpg'],
            ),
            self.create_artwork(
                gallery,
                'Stone Memory',
                'Sculpture',
                'Impressionism',
                '2400.00',
                '35 x 22 x 18 cm',
                2021,
                'Original',
                'Previously held in a private Icelandic collection.',
                ['medium-sculpture.jpg'],
            ),
        ]

        BidFinalization.objects.filter(bid__bidder=collector).delete()
        accepted_bid, _ = Bid.objects.update_or_create(
            artwork=artworks[0],
            bidder=collector,
            defaults={
                'price': '1350.00',
                'expiration': timezone.now() + timedelta(days=10),
                'status': Bid.BidStatus.ACCEPTED,
            },
        )
        Bid.objects.update_or_create(
            artwork=artworks[2],
            bidder=collector,
            defaults={
                'price': '950.00',
                'expiration': timezone.now() + timedelta(days=5),
                'status': Bid.BidStatus.CONTINGENT,
            },
        )
        Bid.objects.update_or_create(
            artwork=artworks[3],
            bidder=collector,
            defaults={
                'price': '500.00',
                'expiration': timezone.now() + timedelta(days=4),
                'status': Bid.BidStatus.PENDING,
            },
        )

        self.stdout.write(self.style.SUCCESS('Seeded ArtVault demo data.'))
        self.stdout.write(f'Demo login: collector / artvault123')
        self.stdout.write(f'Accepted bid ready to finalize: #{accepted_bid.pk}')

    def create_user(self, username, email, name):
        user, _ = User.objects.get_or_create(username=username, defaults={'email': email})
        user.email = email
        user.set_password('artvault123')
        user.save()
        Profile.objects.update_or_create(user=user, defaults={'name': name})
        return user

    def create_seller(self, user, display_name, seller_type, street_name, city, postal_code, bio):
        seller, _ = Seller.objects.update_or_create(
            user=user,
            defaults={
                'display_name': display_name,
                'seller_type': seller_type,
                'address': f'{street_name}, {city} {postal_code}',
                'street_name': street_name,
                'city': city,
                'postal_code': postal_code,
                'bio': bio,
            },
        )
        return seller

    def create_artwork(
        self,
        seller,
        title,
        medium,
        style,
        price,
        dimensions,
        year,
        edition,
        provenance,
        image_names,
    ):
        artwork, _ = Artwork.objects.update_or_create(
            title=title,
            defaults={
                'seller': seller,
                'medium': medium,
                'style': style,
                'price': price,
                'dimensions': dimensions,
                'year': year,
                'edition': edition,
                'provenance': provenance,
            },
        )
        ArtworkImage.objects.filter(artwork=artwork).delete()
        for index, image_name in enumerate(image_names):
            media_name = self.copy_asset('artwork_images', image_name)
            ArtworkImage.objects.create(
                artwork=artwork,
                image=media_name,
                alt_text=title,
                sort_order=index,
            )
        return artwork

    def attach_media(self, instance, field_name, folder, asset_name):
        media_name = self.copy_asset(folder, asset_name)
        setattr(instance, field_name, media_name)
        instance.save(update_fields=[field_name, 'updated_at'])

    def copy_asset(self, folder, asset_name):
        source = Path(settings.BASE_DIR) / asset_name
        destination_dir = Path(settings.MEDIA_ROOT) / folder
        destination_dir.mkdir(parents=True, exist_ok=True)
        destination = destination_dir / asset_name
        if source.exists() and not destination.exists():
            shutil.copyfile(source, destination)
        return f'{folder}/{asset_name}'
