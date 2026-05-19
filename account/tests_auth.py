from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AccountAuthTests(TestCase):
    def test_register_and_login_flow(self):
        # Register a new user
        register_url = reverse('register')
        data = {
            'email': 'testuser@example.com',
            'password': 'StrongPassword!123',
            'confirm_password': 'StrongPassword!123',
        }
        response = self.client.post(register_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        # User should exist
        user = User.objects.filter(email='testuser@example.com').first()
        self.assertIsNotNone(user)

        # Logout then login
        self.client.logout()
        login_url = reverse('login')
        login_data = {'email': 'testuser@example.com', 'password': 'StrongPassword!123'}
        response = self.client.post(login_url, login_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
