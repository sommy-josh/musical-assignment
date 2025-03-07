import pytest
from rest_framework.test import APIClient
from tests.factories import ArtistFactory, AlbumFactory

@pytest.mark.django_db
def test_large_artist_query(benchmark):
    """Benchmark API response time when retrieving 10,000 artists."""

    # Create large dataset
    ArtistFactory.create_batch(10000)

    client = APIClient()

    def fetch_artists():
        response = client.get("/artists/")
        assert response.status_code == 200  # Ensure successful request
        assert len(response.data["results"]) > 0  # Ensure results exist

    benchmark(fetch_artists)
