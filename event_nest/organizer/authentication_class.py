from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from .models import Organizer



class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user=None
        user_id = validated_token.get('user_id')
        try:
                user = Organizer.objects.get(pk=user_id)
        except Organizer.DoesNotExist:
            raise AuthenticationFailed('Organizer does not exist')
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
