from django.db import models
from social_django.models import UserSocialAuth
from organizer.models import EventNestUsers

class CustomUserSocialAuth(models.Model):
    user = models.ForeignKey(EventNestUsers, on_delete=models.CASCADE)
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=255)
    extra_data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'custom_user_social_auth'
