from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from authenticate_.models import Organizer

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token.get('user_id')
        user_type = validated_token.get('user_type')
        
        try:
            if user_type == 'organizer':
                user = Organizer.objects.get(pk=user_id)
            else:
                user = User.objects.get(pk=user_id)
        except (Organizer.DoesNotExist, User.DoesNotExist):
            user = None
        return user

