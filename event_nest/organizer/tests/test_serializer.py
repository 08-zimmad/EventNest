from datetime import datetime, timedelta

from attendee.models import AttendeeEvent
from attendee.tests.factory import AttendeeEventFactory
from django.test import TestCase
from rest_framework import serializers

from ..models import EventNestUsers, Events
from ..serializer import (EventNestUserSerializer, EventsSerializer,
                          OrganizerAttendanceSerializer, GetAttendeeSerializer,
                          EventMediaFilesSerializer)
from .factory import EventNestUserFactory, EventsFactory


class EventNestUserSerializerTest(TestCase):
    def setUp(self):
        self.user_data = EventNestUserFactory.build()

    def test_valid_data(self):
        serializer = EventNestUserSerializer(
            data={
                "name": self.user_data.name,
                "email": self.user_data.email,
                "password": "StrongPassword123",
                "role": self.user_data.role,
                "organization": self.user_data.organization
            }
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertIn("name", serializer.data)
        self.assertIn("email", serializer.data)
        self.assertIn("role", serializer.data)
        self.assertIn("organization", serializer.data)

    def test_invalid_email_format(self):
        serializer = EventNestUserSerializer(
            data={
                "name": self.user_data.name,
                "email": "admin",
                "password": "StrongPassword123",
                "role": self.user_data.role,
                "organization": self.user_data.organization
            }
        )
        self.assertFalse(serializer.is_valid())
        self.assertIsNotNone(serializer.error_messages)
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_empty_email(self):
        serializer = EventNestUserSerializer(
            data={
                "name": self.user_data.name,
                "email": "",
                "password": "StrongPassword123",
                "role": self.user_data.role,
                "organization": self.user_data.organization
            }
        )
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_role(self):
        serializer = EventNestUserSerializer(
            data={
                "name": self.user_data.name,
                "email": self.user_data.email,
                "password": "StrongPassword123",
                "role": "admin",
                "organization": self.user_data.organization
            }
        )
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_missing_name(self):
        serializer = EventNestUserSerializer(
            data={
                "email": self.user_data.email,
                "password": "StrongPassword123",
                "role": self.user_data.role,
                "organization": self.user_data.organization
            }
        )
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_name_format(self):
        serializer = EventNestUserSerializer(
            data={
                "name": 123123,
                "email": self.user_data.email,
                "password": "StrongPassword123",
                "role": "admin",
                "organization": self.user_data.organization
            }
        )
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_missing_not_null_fields(self):
        serializer = EventNestUserSerializer(
            data={
                "name": self.user_data.name,
                "password": "StrongPassword123",
                "role": self.user_data.role,
                "organization": self.user_data.organization
            }
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)


class EventNestUserTestForUpdation(TestCase):
    def setUp(self):
        self.prev_user = EventNestUserFactory.create()
        self.role = None

    def test_full_update_user(self):
        self.role = (
            "organizer" if self.prev_user.role == "attendee" else "attendee"
            )

        updated_data = {
            "name": "updated name2",
            "email": "Updated_email6@example.com",
            "password": "UpdatedPassword1231233",
            "role": self.role,
            "organization": "New Organization6"
        }
        user = EventNestUsers.objects.get(email=self.prev_user.email)
        serializer = EventNestUserSerializer(instance=user,
                                             data=updated_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        self.assertEqual(updated_data["name"], serializer.data['name'])
        self.assertEqual(updated_data["email"], serializer.data['email'])
        self.assertEqual(
            updated_data["organization"],
            serializer.data['organization']
            )

    def test_partial_update(self):
        self.role = (
            "organizer" if self.prev_user.role == "attendee" else "attendee"
            )
        updated_data = {
            "name": "updated name2",
            "role": self.role,
            "organization": "New Organization6"
        }
        serializer = EventNestUserSerializer(instance=self.prev_user,
                                             data=updated_data,
                                             partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(updated_data["name"], serializer.data["name"])
        self.assertEqual(updated_data["role"], serializer.data["role"])
        self.assertEqual(
            updated_data['organization'],
            serializer.data["organization"])


class EventsSerializerTest(TestCase):
    def setUp(self):
        self.organizer = EventNestUserFactory.build()
        self.event = EventsFactory.build(organization=self.organizer)

    def test_valid_data(self):
        data = {
            "title": self.event.title,
            "description": self.event.description,
            "date": self.event.date,
            "time": self.event.time,
            "venue_details": self.event.venue_details,
            "duration": self.event.duration,
        }
        serializer = EventsSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        # date, time, and duration format
        serializer_duration = timedelta(
            hours=int(serializer.data['duration'].split(':')[0]),
            minutes=int(serializer.data['duration'].split(':')[1]),
            seconds=int(serializer.data['duration'].split(':')[2])
            )
        serializer_date = datetime.strptime(
            serializer.data['date'],
            '%Y-%m-%d').date()
        serializer_time = datetime.strptime(
            serializer.data['time'],
            '%H:%M:%S.%f').time()

        self.assertEqual(serializer.data['title'], data['title'])
        self.assertEqual(serializer.data['description'], data['description'])
        self.assertEqual(serializer_date, data['date'])
        self.assertEqual(serializer_time, data['time'])
        self.assertEqual(
            serializer.data['venue_details'],
            data['venue_details'])
        self.assertEqual(serializer_duration, data['duration'])

    def test_invalid_data(self):
        data = {
                "title": "1312312331",
                "description": "4343",
                "date": "2008/14/12",
                "time": "13:60",
                "venue_details": "434343",
                "duration": '12312',
            }
        serialzier = EventsSerializer(data=data)
        self.assertFalse(serialzier.is_valid())

    def test_get_events(self):
        event_fac = EventsFactory.create(title="hahahaha")
        event = Events.objects.get(title=event_fac.title)
        serializer = EventsSerializer(event)
        self.assertIn("title", serializer.data)
        self.assertIn("description", serializer.data)
        self.assertIn("duration", serializer.data)
        self.assertIn("time", serializer.data)
        self.assertIn("date", serializer.data)
        self.assertIn("venue_details", serializer.data)

    def test_event_date_in_past(self):
        past_time = datetime.now() - timedelta(days=1)
        serializer_duration = timedelta(
            hours=self.event.duration.seconds // 3600,
            minutes=(self.event.duration.seconds % 3600) // 60,
            seconds=self.event.duration.seconds % 60,
        )
        serializer_date = past_time.date()
        serializer_time = past_time.time()

        data = {
            "title": self.event.title,
            "description": self.event.description,
            "date": serializer_date,
            "time": serializer_time,
            "venue_details": self.event.venue_details,
            "duration": serializer_duration,
        }
        serializer = EventsSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_event_time_in_past(self):
        past_time = datetime.now() - timedelta(hours=1)
        serializer_duration = timedelta(
            hours=self.event.duration.seconds // 3600,
            minutes=(self.event.duration.seconds % 3600) // 60,
            seconds=self.event.duration.seconds % 60,
        )
        serializer_date = past_time.date()
        serializer_time = past_time.time()
        data = {
            "title": self.event.title,
            "description": self.event.description,
            "date": serializer_date,
            "time": serializer_time,
            "venue_details": self.event.venue_details,
            "duration": serializer_duration,
        }
        serializer = EventsSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)


class AttendanceSerializerTest(TestCase):
    def setUp(self):
        self.organizer = EventNestUserFactory.create(role="organizer")
        self.event_data = EventsFactory.create(registration_count=12,
                                               organization=self.organizer)

    def test_valid_attendance_mark(self):
        data = {
            "present_count": 12}
        serializer = OrganizerAttendanceSerializer(
            instance=self.event_data,
            data=data, partial=True
            )
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_negative_value(self):
        data = {
            "present_count": -1}

        data2 = {
            "present_count": -1}
        serializer = OrganizerAttendanceSerializer(instance=self.event_data,
                                                   data=data,
                                                   partial=True)
        serializer2 = OrganizerAttendanceSerializer(instance=self.event_data,
                                                    data=data2,
                                                    partial=True)

        self.assertFalse(serializer.is_valid())
        self.assertFalse(serializer2.is_valid())

    def test_attendance_invalid_datatype(self):
        data = {
            "present_count": "wowowo"
        }
        serializer = OrganizerAttendanceSerializer(instance=self.event_data,
                                                   data=data,
                                                   partial=True)
        self.assertFalse(serializer.is_valid())


class AttendeeEventSerializerTest(TestCase):

    def setUp(self):
        self.organizer = EventNestUserFactory.create(role="organizer")
        self.event = EventsFactory.create(organization=self.organizer)
        self.registered_attendee = EventNestUserFactory.create_batch(
            10,
            role="attendee")
        self.attendee_event = [
            AttendeeEventFactory.create(
                Attendee=attendee,
                event=self.event
            )
            for attendee in self.registered_attendee
        ]

    def test_get_registered_attendee_list(self):
        events = Events.objects.get(id=self.event.id)
        attendee_events = AttendeeEvent.objects.filter(event=events)
        attendees = [attendee_event.Attendee
                     for attendee_event in attendee_events]
        serializer = GetAttendeeSerializer(attendees, many=True)
        for attendee, registered_attendee in zip(serializer.data,
                                                 self.registered_attendee):
            self.assertEqual(attendee["email"], registered_attendee.email)

    def test_empty_attendee_list_handling(self):
        event = EventsFactory.create()
        events = Events.objects.get(id=event.id)
        attendee_events = AttendeeEvent.objects.filter(event=events)
        serializer = GetAttendeeSerializer(attendee_events, many=True)
        self.assertEqual(serializer.data, [])


class EventMediaFilesSerializerTest(TestCase):

    def setUp(self):
        self.event = EventsFactory.create()

    def test_event_media_files_deserialization(self):
        updated_data = {
            'image': self.event.image,
            'video': self.event.video,
            'file': self.event.file,
        }

        serializer = EventMediaFilesSerializer(
            instance=self.event,
            data=updated_data,
            partial=True)

        # factory saves empty files with correct format
        # serializer generates the error that files are empty
        # thats why given assertFalse
        self.assertFalse(serializer.is_valid())
        self.assertIn("image", serializer.data)
        self.assertIn("video", serializer.data)
        self.assertIn("file", serializer.data)
