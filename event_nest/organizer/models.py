from django.db import models, transaction
from django.contrib.auth.models import AbstractBaseUser
from django.db.transaction import TransactionManagementError
from django.core.validators import MaxValueValidator
from .manager import EventNestUserManager

class EventNestUsers(AbstractBaseUser):

    ROLES = [
        ("attendee", "Attendee"),
        ("organizer", "Organizer")]

    name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    organization = models.CharField(max_length=40, unique=True, null=True)
    role = models.CharField(max_length=20, choices=ROLES, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = EventNestUserManager()

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class Events(models.Model):

    title = models.CharField(max_length=40, unique=True)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    organization = models.ForeignKey(
        EventNestUsers,
        on_delete=models.CASCADE,
        related_name='events_set')
    duration = models.DurationField()
    venue_details = models.TextField()
    registration_count = models.PositiveIntegerField(default=0)
    present_count = models.PositiveIntegerField(default=0)
    image = models.ImageField(null=True, upload_to='image/')
    video = models.FileField(upload_to='videos/', null=True)
    file = models.FileField(upload_to='file/', null=True)
    rating = models.FloatField(default=0.00,
                               validators=[MaxValueValidator(5.00)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


def count_registered_attendees(events):
    try:
        with transaction.atomic():
            event = Events.objects.select_for_update().get(id=events)
            event.registration_count += 1
            event.save()
        return True
    except TransactionManagementError:
        return False
