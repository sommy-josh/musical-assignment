# api/authentication.py

import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import AdminUser

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

        try:
            user = AdminUser.objects.get(id=payload['user_id'])
        except AdminUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        return (user, token)