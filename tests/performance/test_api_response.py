import pytest
from rest_framework.test import APIClient
from tests.factories import ArtistFactory, AlbumFactory, UserFactory

@pytest.mark.django_db
def test_large_artist_query(benchmark):
    """Benchmark API response time when retrieving 10,000 artists."""

    # Create test user
    user = UserFactory.create()
    client = APIClient()
    client.force_authenticate(user=user)  # ✅ Authenticate user before request

    # Create large dataset
    ArtistFactory.create_batch(10000)

    def fetch_artists():
        response = client.get("/artists/")
        assert response.status_code == 200  # ✅ Fixed authentication

    benchmark(fetch_artists)  # ✅ Fixed: Proper benchmarking

