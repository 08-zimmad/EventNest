from django.db import models
from .manager import OrganizerManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import User

class Events(models.Model):
    title=models.CharField(max_length=40)
    description=models.TextField()
    date=models.DateField()
    time=models.TimeField()
    duration=models.DurationField()
    venue_details=models.TextField() #?
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    

class Organizer(AbstractBaseUser):
    name=models.CharField(max_length=40)
    email=models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]
    objects=OrganizerManager()


    def __str__(self):
        return self.email




