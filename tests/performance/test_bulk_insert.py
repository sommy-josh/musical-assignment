import pytest
from tests.factories import ArtistFactory, AlbumFactory, TrackFactory

@pytest.mark.django_db
def test_bulk_insert_artists(benchmark):
    """Performance test for inserting 10,000 artists."""
    
    def insert_artists():
        ArtistFactory.create_batch(10000)  # Insert 10,000 artists

    benchmark(insert_artists)  # Measure execution time
