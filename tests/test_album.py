from rest_framework.test import APITestCase
from rest_framework import status
from .factories import UserFactory, ArtistFactory, AlbumFactory

class AlbumTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.album_url = "/albums/"
        self.artist = ArtistFactory(name="Coldplay")

    def test_create_album(self):
        """Ensure an album can be created"""
        album_data = {"title": "A Rush of Blood to the Head", "release_year": 2002, "artist_id": self.artist.id}
        response = self.client.post(self.album_url, album_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["title"], "A Rush of Blood to the Head")

    def test_get_albums(self):
        """Ensure albums can be retrieved"""
        AlbumFactory(title="X&Y", artist=self.artist, release_year=2005)
        response = self.client.get(self.album_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data["results"]), 0)
