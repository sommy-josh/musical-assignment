from rest_framework.test import APITestCase
from rest_framework import status
from .factories import UserFactory, AlbumFactory, TrackFactory

class TrackTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.track_url = "/tracks/"
        self.album = AlbumFactory(title="Scorpion")

    def test_create_track(self):
        """Ensure a track can be created"""
        track_data = {"title": "God's Plan", "duration": "00:03:31", "file_url": "http://example.com/song.mp3", "album_id": self.album.id}
        response = self.client.post(self.track_url, track_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["title"], "God's Plan")

    def test_get_tracks(self):
        """Ensure tracks can be retrieved"""
        TrackFactory(title="In My Feelings", album=self.album)
        response = self.client.get(self.track_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data["results"]), 0)
