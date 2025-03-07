from rest_framework.test import APITestCase
from rest_framework import status
from .factories import UserFactory, GenreFactory, ArtistFactory

class ArtistTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.artist_url = "/artists/"
        self.genre = GenreFactory(name="Rock")

    def test_create_artist(self):
        """Ensure an artist can be created"""
        artist_data = {"name": "Drake", "bio": "Canadian Rapper", "genre_id": self.genre.id}
        response = self.client.post(self.artist_url, artist_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["name"], "Drake")

    def test_get_artists(self):
        """Ensure artists can be retrieved"""
        ArtistFactory(name="Eminem", genre=self.genre)
        response = self.client.get(self.artist_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data["results"]), 0)
