from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from organizer.models import EventNestUsers


class CustomJWTAuthentication(JWTAuthentication):

    def get_user(self, validated_token):
        user = None
        user_id = validated_token.get('user_id')
        user = get_object_or_404(EventNestUsers, id=user_id)
        return user

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
