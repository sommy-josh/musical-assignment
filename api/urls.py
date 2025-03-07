from django.urls import re_path
from .views import (
    Login, Register,
    GenreListCreateAPIView, GenreDetailAPIView, 
    ArtistListCreateAPIView, AlbumListCreateAPIView, 
    TrackListCreateAPIView
)

urlpatterns = [
    re_path(r'^auth/login/?$', Login.as_view(), name='login'),
    re_path(r'^auth/register/?$', Register.as_view(), name='register'),
    re_path(r'^genres/?$', GenreListCreateAPIView.as_view(), name='genre-list-create'),
    re_path(r'^genres/(?P<genre_id>\d+)/?$', GenreDetailAPIView.as_view(), name='genre-detail'),
    re_path(r'^artists/?$', ArtistListCreateAPIView.as_view(), name='artist-list-create'),
    re_path(r'^albums/?$', AlbumListCreateAPIView.as_view(), name='album-list-create'),
    re_path(r'^tracks/?$', TrackListCreateAPIView.as_view(), name='track-list-create'),
]
