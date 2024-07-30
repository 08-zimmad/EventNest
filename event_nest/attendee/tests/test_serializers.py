from attendee.serializers import (AttendeeProfileSerializer,
                                  AttendeeRegisterToEventSerializer,
                                  GetEventSerializer, RatingSerializer)
from django.test import TestCase
from organizer.tests.factory import EventNestUserFactory, EventsFactory
from organizer.models import Events, EventNestUsers


class AttendeeProfileSerializerTest(TestCase):
    def setUp(self):
        self.user_data = EventNestUserFactory.create(role="attendee")

    def test_get_valid_event(self):
        event = EventNestUsers.objects.get(id=self.user_data.id)
        serializer = AttendeeProfileSerializer(event)
        self.assertIn("name", serializer.data)
        self.assertIn("email", serializer.data)

    def test_update_valid_data(self):
        serializer = AttendeeProfileSerializer(
            instance=self.user_data,
            data={
                "name": "ahmadddd",
                "email": "me@gmail.com"
            },
            partial=True
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertIn("name", serializer.data)
        self.assertIn("email", serializer.data)

    def test_update_invalid_email_format(self):
        serializer = AttendeeProfileSerializer(
            instance=self.user_data,
            data={
                "name": self.user_data.name,
                "email": "invalid_email"
            },
            partial=True
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_empty_email(self):
        serializer = AttendeeProfileSerializer(
            instance=self.user_data,
            data={
                "name": self.user_data.name,
                "email": ""
            },
            partial=True
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)


class GetEventSerializerTest(TestCase):
    def setUp(self):
        self.organizer = EventNestUserFactory.create()
        self.event = EventsFactory.create(organization=self.organizer)

    def test_valid_data(self):
        event = Events.objects.get(id=self.event.id)
        serializer = GetEventSerializer(event)
        self.assertIn("title", serializer.data)
        self.assertIn("description", serializer.data)
        self.assertIn("date", serializer.data)
        self.assertIn("time", serializer.data)
        self.assertIn("venue_details", serializer.data)
        self.assertIn("organization", serializer.data)


class AttendeeRegisterToEventSerializerTest(TestCase):
    def setUp(self):
        self.organizer = EventNestUserFactory.create(role="organizer")
        self.event = EventsFactory.create(organization=self.organizer)
        self.attendee = EventNestUserFactory.create(role="attendee")

    def test_valid_registration(self):
        data = {
            "Attendee": self.attendee.id,
            "event": self.event.id
        }
        serializer = AttendeeRegisterToEventSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.data['Attendee'], data['Attendee'])
        self.assertEqual(serializer.data['event'], data['event'])

    def test_invalid_registration(self):
        data = {
            "Attendee": None,
            "event": None
        }
        serializer = AttendeeRegisterToEventSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Attendee", serializer.errors)
        self.assertIn("event", serializer.errors)


class RatingSerializerTest(TestCase):
    def setUp(self):
        self.event = EventsFactory.create()

    def test_valid_rating(self):
        data = {
            "rating": 4.5
        }
        serializer = RatingSerializer(
            instance=self.event,
            data=data,
            partial=True
            )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        self.assertEqual(serializer.data['rating'], data['rating'])

    def test_invalid_rating(self):
        data = {"rating": 6.0}
        serializer = RatingSerializer(
            instance=self.event,
            data=data,
            partial=True
            )
        self.assertFalse(serializer.is_valid())
        self.assertIn("rating", serializer.errors)
