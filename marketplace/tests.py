from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Artwork, Bid, BidFinalization, Favorite, Profile, Seller


class MarketplaceFlowTests(TestCase):
    def setUp(self):
        self.collector = User.objects.create_user(
            username='collector',
            email='collector@example.com',
            password='artvault123',
        )
        self.seller_user = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='artvault123',
        )
        Profile.objects.create(user=self.collector, name='Marta Collector')
        Profile.objects.create(user=self.seller_user, name='Nordic Gallery')
        self.seller = Seller.objects.create(
            user=self.seller_user,
            display_name='Nordic Gallery',
            seller_type=Seller.SellerType.GALLERY,
            address='Austurstraeti 12, Reykjavik 101',
            street_name='Austurstraeti 12',
            city='Reykjavik',
            postal_code='101',
            bio='Contemporary gallery.',
        )
        self.oil = Artwork.objects.create(
            seller=self.seller,
            title='Red Bloom',
            medium='Oil',
            style='Abstract',
            price='1200.00',
            dimensions='80 x 60 cm',
            year=2024,
        )
        self.photo = Artwork.objects.create(
            seller=self.seller,
            title='Blue Valley',
            medium='Photography',
            style='Modern',
            price='900.00',
            dimensions='70 x 50 cm',
            year=2023,
        )

    def test_catalogue_filters_by_title_and_medium(self):
        response = self.client.get(
            reverse('marketplace:artwork_list'),
            {'q': 'red', 'medium': 'Oil'},
        )

        self.assertContains(response, 'Red Bloom')
        self.assertNotContains(response, 'Blue Valley')

    def test_submit_bid_requires_login(self):
        response = self.client.get(reverse('marketplace:submit_bid', args=[self.oil.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response['Location'])

    def test_logged_in_user_can_submit_bid(self):
        self.client.login(username='collector', password='artvault123')
        response = self.client.post(
            reverse('marketplace:submit_bid', args=[self.photo.pk]),
            {
                'price': '950.00',
                'expiration': (timezone.now() + timedelta(days=5)).strftime('%Y-%m-%dT%H:%M'),
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Bid.objects.filter(
                artwork=self.photo,
                bidder=self.collector,
                price='950.00',
                status=Bid.BidStatus.PENDING,
            ).exists()
        )

    def test_logged_in_user_can_add_and_remove_favorite(self):
        self.client.login(username='collector', password='artvault123')

        add_response = self.client.post(
            reverse('marketplace:toggle_favorite', args=[self.oil.pk]),
        )

        self.assertEqual(add_response.status_code, 302)
        self.assertTrue(
            Favorite.objects.filter(
                artwork=self.oil,
                user=self.collector,
            ).exists()
        )

        remove_response = self.client.post(
            reverse('marketplace:toggle_favorite', args=[self.oil.pk]),
        )

        self.assertEqual(remove_response.status_code, 302)
        self.assertFalse(
            Favorite.objects.filter(
                artwork=self.oil,
                user=self.collector,
            ).exists()
        )

    def test_favorites_page_lists_user_favorites(self):
        Favorite.objects.create(artwork=self.photo, user=self.collector)
        self.client.login(username='collector', password='artvault123')

        response = self.client.get(reverse('marketplace:favorite_list'))

        self.assertContains(response, 'Blue Valley')
        self.assertNotContains(response, 'Red Bloom')

    def test_finalize_accepted_bid(self):
        bid = Bid.objects.create(
            artwork=self.oil,
            bidder=self.collector,
            price='1300.00',
            expiration=timezone.now() + timedelta(days=7),
            status=Bid.BidStatus.ACCEPTED,
        )
        self.client.login(username='collector', password='artvault123')

        self.client.post(
            reverse('marketplace:finalize_bid_step', args=[bid.pk, 'contact']),
            {
                'street_name': 'Main Street 1',
                'city': 'Reykjavik',
                'postal_code': '101',
                'country': 'Iceland',
                'national_id': '010190-1234',
            },
        )
        self.client.post(
            reverse('marketplace:finalize_bid_step', args=[bid.pk, 'payment']),
            {
                'payment_method': 'bank_transfer',
                'bank_account': '0000-00-123456',
            },
        )
        response = self.client.post(reverse('marketplace:finalize_bid_step', args=[bid.pk, 'review']))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            BidFinalization.objects.filter(
                bid=bid,
                finalized_at__isnull=False,
                payment_method='bank_transfer',
            ).exists()
        )
