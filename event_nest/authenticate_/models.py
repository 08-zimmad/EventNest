from django.db import models
from .manager import OrganizerManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings


class Organizer(AbstractBaseUser):
    name=models.CharField(max_length=40)
    email=models.EmailField(unique=True)
    organization=models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]
    objects=OrganizerManager()


    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    


class Events(models.Model):
    title=models.CharField(max_length=40)
    description=models.TextField()
    date=models.DateField()
    time=models.TimeField()
    organization=models.ForeignKey(Organizer,on_delete=models.CASCADE, related_name='events_set')
    duration=models.DurationField()
    venue_details=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    


