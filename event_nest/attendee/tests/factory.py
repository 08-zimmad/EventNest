import factory
from attendee.models import AttendeeEvent, EmailTemplate
from organizer.tests.factory import (EventNestUserFactory, EventsFactory)


class AttendeeEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttendeeEvent

    Attendee = factory.SubFactory(EventNestUserFactory)
    event = factory.SubFactory(EventsFactory)


class EmailTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmailTemplate

    subject = factory.Faker("sentence", nb_words=3)
    template = factory.Faker("text")
