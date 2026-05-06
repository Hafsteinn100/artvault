from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    def test_homepage_renders_artvault_homepage(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buy or sell art')
        self.assertContains(response, 'Latest Pieces')
        self.assertContains(response, 'Amber Stillness')
