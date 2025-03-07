import base64
from datetime import datetime, timedelta
from django.conf import settings
from django.shortcuts import get_object_or_404
import jwt
from django.contrib.auth import authenticate
import uuid
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db.models import Q
from api.filters import filter_queryset
from .models import Artist, Album, Track, Genre, User, UserProfile
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer, GenreSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from .pagination import StandardResultsSetPagination
from utils.helper import generate_random_username


ACCESS_TOKEN_EXPIRATION = timedelta(weeks=53)
REFRESH_TOKEN_EXPIRATION = timedelta(weeks=53)
JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = "HS256"


def generate_access_token(user):
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.utcnow() + ACCESS_TOKEN_EXPIRATION,
        'type': 'access'
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def generate_refresh_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + REFRESH_TOKEN_EXPIRATION,
        'type': 'refresh'
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


class Register(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic  # Wrap the entire registration process in a transaction
    def post(self, request):
        try:
            email = request.data.get('email', None)
            password = request.data.get('password', None)
            first_name = request.data.get("first_name", None)
            last_name = request.data.get('last_name', None)

            if not email or not password:
                return Response({'status': False, 'message': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

            email = email.lower()
            username = generate_random_username(last_name.lower())  # Generate a random username
            user_uuid = uuid.uuid4()

            # Create the user
            user = User.objects.create_user(
                email=email,
                username=username,
                first_name=first_name.title(),
                last_name=last_name.title(),
                user_uid=user_uuid
            )
            user.set_password(password)
            user.save()

            # Create user profile
            UserProfile.objects.create(user=user)

            # Generate access and refresh tokens
            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)

            return Response({
                'status': True,
                'message': 'Registration successful.',
                'data': {
                    'user_id': str(user.user_uid),
                    'email': user.email,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'date_created': user.date_joined,
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'status': False, 'message': 'Registration failed.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        login_id = request.data.get('login_id', None)
        password = request.data.get('password', None)

        if not login_id or not password:
            return Response({'status': False, 'message': 'Login ID and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        login_id_lower = login_id.lower()  # Convert to lowercase for email, username, and UUID searches
        login_id_title = login_id.title()  # Convert to title case for first name and last name searches

        # Try finding the user with multiple possible identifiers
        user = User.objects.filter(
            Q(email__iexact=login_id_lower) |  # Case-insensitive email search
            Q(username__iexact=login_id_lower) |  # Case-insensitive username search
            Q(user_uid__iexact=login_id_lower) |  # Case-insensitive UUID search
            Q(first_name=login_id_title) |  # Title case search for first name
            Q(last_name=login_id_title)  # Title case search for last name
        ).first()

        if not user:
            return Response({'status': False, 'message': 'Invalid login credentials'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user with email (since Django `authenticate` expects email or username)
        user = authenticate(email=user.email, password=password)
        if not user:
            return Response({'status': False, 'message': 'Invalid login credentials'}, status=status.HTTP_400_BAD_REQUEST)

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        # Force Authenticator App MFA
        return Response({
                'status': True,
                'message': 'Login successful',
                'data': {
                    'user_id': user.user_uid,
                    'email': user.email,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'date_created': user.date_joined,
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                }
            }, status=status.HTTP_200_OK)


# ======= Genre API =======
class GenreListCreateAPIView(APIView, StandardResultsSetPagination):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Genre.objects.all()

        # Filtering by Genre Name
        genre_name = request.query_params.get('genre', None)
        if genre_name:
            queryset = queryset.filter(name__icontains=genre_name)

        results = self.paginate_queryset(queryset, request, view=self)
        serializer = GenreSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Genre created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message": "Validation error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class GenreDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, genre_id):
        try:
            return Genre.objects.get(id=genre_id)
        except Genre.DoesNotExist:
            return None

    def get(self, request, genre_id):
        genre = self.get_object(genre_id)
        if not genre:
            return Response({"status": False, "message": "Genre not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GenreSerializer(genre)
        return Response({"status": True, "data": serializer.data})

    def put(self, request, genre_id):
        genre = self.get_object(genre_id)
        if not genre:
            return Response({"status": False, "message": "Genre not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GenreSerializer(genre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Genre updated successfully", "data": serializer.data})
        return Response({"status": False, "message": "Validation error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, genre_id):
        genre = self.get_object(genre_id)
        if not genre:
            return Response({"status": False, "message": "Genre not found"}, status=status.HTTP_404_NOT_FOUND)
        genre.delete()
        return Response({"status": True, "message": "Genre deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ======= Artist API =======
class ArtistListCreateAPIView(APIView, StandardResultsSetPagination):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Artist.objects.all()

        # Filtering by Artist Name
        artist_name = request.query_params.get('artist_name', None)
        if artist_name:
            queryset = queryset.filter(name__icontains=artist_name)

        # Filtering by Genre Name
        genre_name = request.query_params.get('genre', None)
        if genre_name:
            queryset = queryset.filter(genre__name__icontains=genre_name)

        results = self.paginate_queryset(queryset, request, view=self)
        serializer = ArtistSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Artist created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message": "Validation error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# ======= Album API =======
class AlbumListCreateAPIView(APIView, StandardResultsSetPagination):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Album.objects.all()

        # Filtering by Album Title
        album_title = request.query_params.get('album_title', None)
        if album_title:
            queryset = queryset.filter(title__icontains=album_title)

        # Filtering by Release Year Range
        start_year = request.query_params.get('start_year', None)
        end_year = request.query_params.get('end_year', None)

        if start_year and start_year.isdigit():
            queryset = queryset.filter(release_year__gte=int(start_year))
        if end_year and end_year.isdigit():
            queryset = queryset.filter(release_year__lte=int(end_year))

        # Filtering by Artist Name
        artist_name = request.query_params.get('artist_name', None)
        if artist_name:
            queryset = queryset.filter(artist__name__icontains=artist_name)

        # Sorting Albums by Release Year
        sort_order = request.query_params.get('sort', 'desc').lower()  # Default: Newest First
        if sort_order == 'asc':
            queryset = queryset.order_by('release_year')  # Oldest First
        else:
            queryset = queryset.order_by('-release_year')  # Newest First

        results = self.paginate_queryset(queryset, request, view=self)
        serializer = AlbumSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Album created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message": "Validation error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# ======= Track API =======
class TrackListCreateAPIView(APIView, StandardResultsSetPagination):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Track.objects.all()

        # Filtering by Track Title
        track_title = request.query_params.get('track_title', None)
        if track_title:
            queryset = queryset.filter(title__icontains=track_title)

        # Filtering by Album Title
        album_title = request.query_params.get('album_title', None)
        if album_title:
            queryset = queryset.filter(album__title__icontains=album_title)

        # Filtering by Artist Name
        artist_name = request.query_params.get('artist_name', None)
        if artist_name:
            queryset = queryset.filter(album__artist__name__icontains=artist_name)

        # Sorting Tracks by Album Release Year
        sort_order = request.query_params.get('sort', 'desc').lower()
        if sort_order == 'asc':
            queryset = queryset.order_by('album__release_year')  # Oldest First
        else:
            queryset = queryset.order_by('-album__release_year')  # Newest First

        results = self.paginate_queryset(queryset, request, view=self)
        serializer = TrackSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = TrackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Track created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message": "Validation error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
