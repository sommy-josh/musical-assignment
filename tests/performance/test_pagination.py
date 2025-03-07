import pytest
from rest_framework.test import APIClient
from tests.factories import TrackFactory

@pytest.mark.django_db
def test_pagination_performance(benchmark):
    """Benchmark pagination performance with 10,000 tracks."""

    # Create large dataset
    TrackFactory.create_batch(10000)

    client = APIClient()

    def fetch_paginated_tracks():
        response = client.get("/tracks/?limit=100")
        assert response.status_code == 200
        assert len(response.data["results"]) == 100  # Ensure pagination works

    benchmark(fetch_paginated_tracks)
