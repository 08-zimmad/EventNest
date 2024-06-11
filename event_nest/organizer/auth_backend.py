from django.contrib.auth.backends import ModelBackend
from .models import Organizer
from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend
from organizer.models import Organizer
from drf_social_oauth2.authentication import SocialAuthentication
from oauth2_provider.models import AccessToken
from django.utils import timezone



class OrganizerBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Organizer.objects.get(email=email)
            if user.check_password(password):
                return user
        except Organizer.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Organizer.objects.get(pk=user_id)
        except Organizer.DoesNotExist:
            return None



class UserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user=User.objects.get(username=username)

            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

