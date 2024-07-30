from django.db import models
from organizer.models import Events, EventNestUsers


class AttendeeEvent(models.Model):
    Attendee = models.ForeignKey(EventNestUsers, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['Attendee', 'event'])
        ]


class EmailTemplate(models.Model):
    subject = models.CharField(max_length=60, null=False)
    template = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
