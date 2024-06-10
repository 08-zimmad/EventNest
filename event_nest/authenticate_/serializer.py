from rest_framework import serializers
from .models import Organizer,Events
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = [ 'name','email', 'password', 'is_active', 'is_staff',"organization"]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True},
        }

    def create(self, validated_data):
        user = Organizer.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password'],
            organization=validated_data['organization']
        )
        return user



    
class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Events
        fields=['title','description','date','time','duration','venue_details']





class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
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
        # Add custom claims
        token['user_type'] = 'organizer' if hasattr(user, 'organization') else 'user'
        return token





class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        refresh = attrs['refresh']
        token = RefreshToken(refresh)

        data = {
            'access': str(token.access_token)
        }


        # Optionally, add custom claims to the new access token
        user = self.context['request'].user
        token['user_type'] = 'organizer' if hasattr(user, 'organization') else 'user'

        return data