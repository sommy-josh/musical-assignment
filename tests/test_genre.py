from rest_framework.test import APITestCase
from rest_framework import status
from tests.factories import UserFactory, GenreFactory

class GenreTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.genre_url = "/genres/"
        self.genre_data = {"name": "Hip-Hop"}

    def test_create_genre(self):
        """Ensure a genre can be created"""
        response = self.client.post(self.genre_url, self.genre_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["name"], "Hip-Hop")

    def test_get_genres(self):
        """Ensure genres can be retrieved"""
        GenreFactory(name="Jazz")  # Create sample genre
        response = self.client.get(self.genre_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data["results"]), 0)
