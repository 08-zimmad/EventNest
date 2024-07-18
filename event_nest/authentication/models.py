from django.db import models
from organizer.models import EventNestUsers

class CustomUserSocialAuth(models.Model):
    user = models.ForeignKey(EventNestUsers, on_delete=models.CASCADE, related_name='social_auth')
    provider = models.CharField(max_length=255)
    uid = models.CharField(max_length=255)
    extra_data = models.JSONField(default=dict)

    class Meta:
        unique_together = ('provider', 'uid')

    def __str__(self):
        return f'{self.user.email} - {self.provider}'
