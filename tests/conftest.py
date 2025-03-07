import pytest
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music.settings")
django.setup()

@pytest.fixture(scope="class")  # Ensure class-scoped fixture
def django_db_setup():
    pass  # This will allow class-scoped tests to use database setup
