from attendee.tests.factory import AttendeeEventFactory
from attendee.utils.token import get_access_token
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .factory import EventNestUserFactory, EventsFactory


class EventNestRegisterViewTest(APITestCase):

    def setUp(self):
        self.url = reverse("eventnest-register-view")
        self.user_data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "StrongPassword123",
            "role": "attendee",
            "organization": "Test Organization"
        }

    def test_successful_registration(self):
        response = self.client.post(self.url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

    def test_registration_with_existing_email(self):
        EventNestUserFactory(email=self.user_data['email'])
        response = self.client.post(self.url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)


class GetEventViewTest(APITestCase):

    def setUp(self):
        self.user = EventNestUserFactory(role="organizer")
        self.event = EventsFactory(organization=self.user)
        self.url = reverse("get-event-view", kwargs={'pk': self.event.id})
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " +
                                get_access_token(self.user)['access'])

    def test_get_specific_event(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.data)
        self.assertIn("description", response.data)

    def test_get_event_with_invalid_id(self):
        url = reverse("get-event-view", kwargs={'pk': 9999})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)


class EventViewTest(APITestCase):

    def setUp(self):
        self.user = EventNestUserFactory(role="organizer")
        self.url = reverse("event-view")
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " +
            get_access_token(self.user)['access'])

    def test_get_events(self):
        EventsFactory.create_batch(3, organization=self.user)
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_events_no_events(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn("error", response.data)

    def test_create_event(self):
        event = EventsFactory.create(organization=self.user)
        event_data = {
            "title": "sjnsdddfjgdsj",
            "description": event.description,
            "date": event.date,
            "time": event.time,
            "duration": event.duration,
            "venue_details": event.venue_details,
        }

        response = self.client.post(self.url, event_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Success", response.data)

    def test_update_event(self):
        event = EventsFactory.create(organization=self.user)
        updated_data = {
            "title": "sjnsdddfjgdsj",
            "description": "description",
            "date": "2025-10-14",
            "time": "23:34:55",
            "duration": "60",
            "venue_details": "event.venue_details",
        }
        url = reverse("event-view-with-id",
                      kwargs={'pk': event.id})
        response = self.client.put(url, data=updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], updated_data['title'])

    def test_partial_update_event(self):
        event = EventsFactory(organization=self.user)
        url = reverse("event-view-with-id", kwargs={'pk': event.id})
        partial_data = {
            "description": "Partially Updated Description"
        }
        response = self.client.patch(url, partial_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("success", response.data)

    def test_delete_event(self):
        event = EventsFactory(organization=self.user)
        url = reverse("event-view-with-id", kwargs={'pk': event.id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("success", response.data)


class UpdateProfileViewTest(APITestCase):

    def setUp(self):
        self.user = EventNestUserFactory(role="organizer")
        self.url = reverse("update-profile-view")
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " +
            get_access_token(self.user)['access'])

    def test_get_profile(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("name", response.data)

    def test_update_profile(self):
        update_data = {
            "name": "Updated Name",
            "email": "updatedemail@example.com"
        }
        response = self.client.post(self.url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("name", response.data)
        self.assertIn("email", response.data)


class MarkAttendanceViewTest(APITestCase):

    def setUp(self):
        self.user = EventNestUserFactory(role="organizer")
        self.event = EventsFactory(organization=self.user,
                                   registration_count=10)
        self.url = reverse("mark-attendance-view",
                           kwargs={'pk': self.event.id})
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " +
            get_access_token(self.user)['access'])

    def test_mark_attendance_success(self):
        data = {
            "present_count": 10
        }
        response = self.client.post(self.url,
                                    data,
                                    format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(response.data['present_count'],
                         data['present_count'])

    def test_mark_attendance_greater_than_registration(self):
        data = {
            "present_count": self.event.registration_count + 1
        }
        response = self.client.post(self.url,
                                    data,
                                    format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_mark_attendance_in_negative_values(self):
        data = {
            "present_count": -1
        }
        response = self.client.post(self.url,
                                    data,
                                    format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)


class UploadMediaFilesViewTest(APITestCase):

    def setUp(self):
        self.user = EventNestUserFactory(role="organizer")
        self.event = EventsFactory(organization=self.user)
        self.url = reverse("upload-media-files-view",
                           kwargs={'pk': self.event.id})
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " +
            get_access_token(self.user)['access'])

    def test_upload_empty_files(self):
        media_data = {
            "image": self.event.image,
            "video": self.event.video,
            "file": self.event.file
        }
        response = self.client.post(self.url,
                                    media_data, format="multipart")
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["video"][0]),
                         "The submitted file is empty.")
        self.assertEqual(str(response.data["file"][0]),
                         "The submitted file is empty.")


class RegisteredAttendeeViewTest(APITestCase):

    def setUp(self):
        self.user = EventNestUserFactory(role="organizer")
        self.event = EventsFactory(organization=self.user)
        self.attendee = EventNestUserFactory(role="attendee")
        AttendeeEventFactory(Attendee=self.attendee,
                             event=self.event)
        self.url = reverse("registered-attendee-view",
                           kwargs={'pk': self.event.id})
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " +
            get_access_token(self.user)['access'])

    def test_get_registered_attendees(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], self.attendee.email)

    def test_get_zero_registered_attendees(self):
        event = EventsFactory(organization=self.user)
        url = reverse("registered-attendee-view", kwargs={'pk': event.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_invalid_event(self):
        url = reverse("registered-attendee-view", kwargs={'pk': 11212})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
