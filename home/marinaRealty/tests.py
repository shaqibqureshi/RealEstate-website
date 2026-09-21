from django.test import TestCase
from django.urls import reverse

from .models import Property


class PropertyShareTests(TestCase):
    def setUp(self):
        self.property = Property.objects.create(
            title='Beachside Villa',
            location='Malad East, Mumbai',
            description='A lovely 2 BHK with sea views.',
            price=15000000,
            listing_type='buying',
            status='For Sale',
            bedrooms=2,
            bathrooms=2,
            area_sqft=1100,
        )

    def test_share_url_contains_property_link(self):
        url = self.property.get_whatsapp_share_url()
        self.assertTrue(url.startswith('https://wa.me/?'))
        self.assertIn('Check+out+this+property', url)
        self.assertIn(reverse('property_detail', args=[self.property.pk]).replace('/', '%2F'), url)

    def test_detail_page_has_og_tags_and_share_button(self):
        response = self.client.get(
            reverse('property_detail', args=[self.property.pk])
        )
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        for needle in ('og:title', 'og:description', 'og:url', 'wa.me/?', 'Share on WhatsApp'):
            self.assertIn(needle, html)

    def test_list_page_cards_have_share_button(self):
        response = self.client.get(reverse('properties'))
        self.assertContains(response, 'Share on WhatsApp')

    def test_related_cards_render_share_button(self):
        Property.objects.create(
            title='Another Villa',
            location='Bandra West',
            price=9000000,
            listing_type='buying',
        )
        response = self.client.get(
            reverse('property_detail', args=[self.property.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Share on WhatsApp')