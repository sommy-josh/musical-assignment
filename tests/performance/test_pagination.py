import pytest
from rest_framework.test import APIClient
from tests.factories import TrackFactory, UserFactory

@pytest.mark.django_db
def test_pagination_performance(benchmark):
    """Benchmark pagination performance with 10,000 tracks."""

    # Create test user
    user = UserFactory.create()
    client = APIClient()
    client.force_authenticate(user=user)  # ✅ Authenticate user before request

    # Create large dataset
    TrackFactory.create_batch(10000)

    def fetch_paginated_tracks():
        response = client.get("/tracks/?limit=100")
        assert response.status_code == 200  # ✅ Ensure success
        assert 50 <= len(response.data["results"]) <= 100  # ✅ Allow range check

    benchmark(fetch_paginated_tracks)
