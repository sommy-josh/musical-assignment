from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.register_url = "/auth/register/"
        self.login_url = "/auth/login/"
        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "User"
        }

    def test_register_user(self):
        """Ensure a user can register"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access_token", response.data["data"])

    def test_login_user(self):
        """Ensure a user can log in"""
        self.client.post(self.register_url, self.user_data)  # Register first
        login_data = {
            "login_id": "testuser@example.com",
            "password": "testpass123"
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data["data"])
