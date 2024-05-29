from django.contrib.auth.backends import ModelBackend
from .models import Organizer

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
