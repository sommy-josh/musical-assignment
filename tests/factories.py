import datetime
import factory
from django.contrib.auth import get_user_model
from api.models import Genre, Artist, Album, Track

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True  # ✅ Fixes the warning

    email = factory.Sequence(lambda n: f"user{n}@example.com")  # ✅ Ensure unique emails
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.PostGenerationMethodCall("set_password", "testpassword")

class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre

    name = factory.Sequence(lambda n: f"Genre {n}")  # Ensures uniqueness

class ArtistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Artist

    name = factory.Faker("name")
    bio = factory.Faker("text")
    genre = factory.SubFactory(GenreFactory)

class AlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Album

    title = factory.Faker("sentence", nb_words=3)
    release_year = factory.Faker("year")
    artist = factory.SubFactory(ArtistFactory)

class TrackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Track

    title = factory.Faker("sentence", nb_words=2)
    duration = datetime.timedelta(minutes=3, seconds=30)  # ✅ Fixed
    file_url = "http://example.com/song.mp3"
    album = factory.SubFactory(AlbumFactory)
