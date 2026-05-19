from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AccountFlowTests(TestCase):
	def test_register_creates_user_and_redirects_home(self):
		response = self.client.post(
			reverse('register'),
			{
				'email': 'user@example.com',
				'password': 'StrongPassword123!',
				'confirm_password': 'StrongPassword123!',
			},
		)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse('home'))
		self.assertTrue(User.objects.filter(email='user@example.com').exists())

	def test_login_rejects_invalid_credentials(self):
		User.objects.create_user(
			username='user@example.com',
			email='user@example.com',
			password='StrongPassword123!',
		)

		response = self.client.post(
			reverse('login'),
			{'email': 'user@example.com', 'password': 'wrong-password'},
		)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse('login'))

	def test_logout_requires_post(self):
		user = User.objects.create_user(
			username='user2@example.com',
			email='user2@example.com',
			password='StrongPassword123!',
		)
		self.client.force_login(user)

		get_response = self.client.get(reverse('logout'))
		self.assertEqual(get_response.status_code, 405)

		post_response = self.client.post(reverse('logout'))
		self.assertEqual(post_response.status_code, 302)
		self.assertEqual(post_response.url, reverse('login'))
