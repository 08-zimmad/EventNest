from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer
    )
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import serializers


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                email=email,
                password=password
                )
            if not user:
                raise serializers.ValidationError(
                    {'error': 'Invalid credentials'}
                )

            refresh = self.get_token(user)

            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return data
        else:
            raise serializers.ValidationError(
                {'error': 'Must include "email" and "password".'}
            )

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_type'] = (
            'Organizer' if hasattr(user, 'organization') else 'Attendee'
        )
        return token


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = attrs['refresh']
        token = RefreshToken(refresh)

        data = {
            'access': str(token.access_token)
        }
        user = self.context['request'].user
        token['user_type'] = (
            'Organizer' if hasattr(user, 'organization') else 'Attendee'
        )
        return data
