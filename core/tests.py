from django.test import TestCase
from django.urls import reverse


class CoreViewTests(TestCase):
	def test_home_page_is_public_landing(self):
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 200)

	def test_health_check_returns_ok(self):
		response = self.client.get(reverse('health_check'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json().get('status'), 'ok')

	def test_prompts_page_requires_login(self):
		response = self.client.get(reverse('prompts'))
		self.assertEqual(response.status_code, 302)
		self.assertIn(reverse('login'), response.url)
