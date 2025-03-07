from rest_framework import serializers
from .models import Artist, Album, Track, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class ArtistSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    genre_id = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), source="genre", write_only=True)

    class Meta:
        model = Artist
        fields = ['id', 'name', 'bio', 'genre', 'genre_id']

class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    artist_id = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all(), source="artist", write_only=True)

    class Meta:
        model = Album
        fields = ['id', 'title', 'release_year', 'artist', 'artist_id']

class TrackSerializer(serializers.ModelSerializer):
    album = AlbumSerializer(read_only=True)
    album_id = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all(), source="album", write_only=True)

    class Meta:
        model = Track
        fields = ['id', 'title', 'duration', 'file_url', 'album', 'album_id']
