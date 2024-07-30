from unittest.mock import patch

from attendee.models import AttendeeEvent
from attendee.utils.token import get_access_token
from django.conf import settings
from django.urls import reverse
from organizer.models import Events
from organizer.tests.factory import EventNestUserFactory, EventsFactory
from rest_framework import status
from rest_framework.test import APITestCase

from .factory import AttendeeEventFactory, EmailTemplateFactory


class AttendeeRegistrationViewTest(APITestCase):

    def setUp(self):
        self.url = reverse("attendee-signup-view")

        self.attendee_data = {
            "name": "Zimmad",
            "email": "fingerlicking@gmail.com",
            "password": "StrongPassword123",
            "role": "attendee",
            "organization": None
        }

    def test_attendee_failed_signup_post_missing_email(self):
        invalid_data = self.attendee_data.copy()
        invalid_data["email"] = ""
        response = self.client.post(self.url, invalid_data, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn("email", response.data)

    def test_attendee_failed_signup_post_invalid_email_format(self):
        invalid_data = self.attendee_data.copy()
        invalid_data["email"] = "invalid-email-format"
        response = self.client.post(self.url, invalid_data, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn("email", response.data)

    def test_attendee_failed_signup_post_missing_name(self):
        invalid_data = self.attendee_data.copy()
        invalid_data["name"] = ""
        response = self.client.post(self.url, invalid_data, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn("name", response.data)

    def test_attendee_success_signup_post(self):
        response = self.client.post(
            self.url,
            self.attendee_data,
            format="json"
            )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

    def test_attendee_success_signup_post_no_organization(self):
        data_without_org = self.attendee_data.copy()
        del data_without_org["organization"]
        response = self.client.post(self.url, data_without_org, format="json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)


class EventViewTest(APITestCase):

    def setUp(self):
        self.event = EventsFactory.create()
        self.attendee = EventNestUserFactory.create(role="attendee")
        self.email_template = EmailTemplateFactory.create()
        self.url = reverse(
            "events-attendee-registration",
            kwargs={'pk': self.event.id}
            )

    def test_get_specific_event_success_get(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " +
            get_access_token(self.attendee)["access"]
        )
        response = self.client.get(self.url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn("title", response.data)
        self.assertIn("description", response.data)
        self.assertIn("date", response.data)
        self.assertIn("time", response.data)
        self.assertIn("duration", response.data)
        self.assertIn("venue_details", response.data)

    def test_get_specific_event_with_invalid_id_get(self):
        url = reverse("events-attendee-registration", kwargs={'pk': 223})
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " +
            get_access_token(self.attendee)["access"]
        )
        response = self.client.get(url, format="json")
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertIn("detail", response.data)

    @patch("attendee.views.send_email_to_attendee")
    def test_attendee_event_registration_success_post(self, mock_email):
        data = {
            "Attendee": self.attendee.email,
        }
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " +
            get_access_token(self.attendee)["access"]
        )
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'], "Registered Successfully")
        mock_email.assert_called_once_with(self.email_template.subject,
                                           self.email_template.template,
                                           settings.EMAIL_HOST_USER,
                                           str(self.attendee.email))

    @patch("attendee.utils.email.send_email_to_attendee")
    def test_attendee_already_registered_post(self, mock_email):

        AttendeeEventFactory.create(Attendee=self.attendee, event=self.event)
        data = {
            "Attendee": self.attendee.email,
        }
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " +
            get_access_token(self.attendee)["access"]
        )
        response = self.client.post(
            self.url,
            data=data,
            format="json"
            )
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
            )
        self.assertIn("data", response.data)
        self.assertEqual(response.data['data'], "Already Registered")
        mock_email.assert_not_called()

    def test_post_without_authentication(self):
        data = {
            "Attendee": self.attendee.email,
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_event_success(self):
        organizer = EventNestUserFactory.create(role="organizer")
        event = EventsFactory.create(organization=organizer)
        attendee = EventNestUserFactory.create(role="attendee")
        url = reverse("events-attendee-registration", kwargs={'pk': event.id})
        AttendeeEventFactory.create(Attendee=attendee, event=event)
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " +
            get_access_token(attendee)["access"]
        )
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(AttendeeEvent.DoesNotExist):
            AttendeeEvent.objects.get(Attendee=attendee, event=self.event)

    def test_delete_event_with_invalid_id(self):
        url = reverse(
            "events-attendee-registration",
            kwargs={'pk': 1123}
            )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " +
            get_access_token(self.attendee)["access"]
        )
        response = self.client.delete(url, format="json")
        qs = AttendeeEvent.objects.filter(
            Attendee=self.attendee,
            event=self.event
            )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(qs.exists())


class FetchAllEventsViewsTest(APITestCase):

    def setUp(self):
        self.url = reverse("get-all-events-available-view")
        self.user = EventNestUserFactory.create(role="attendee")
        self.events = EventsFactory.create_batch(10, organization=self.user)

    def test_get_all_events_success(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " +
            get_access_token(self.user)["access"]
        )
        response = self.client.get(self.url, format="json")
        events = Events.objects.all().count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(events, 10)

    def test_get_events_with_unauthenticated_user(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, 401)
        self.assertIn("detail", response.data)

    def test_get_all_event_with_authorized_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, 200)
        returned_events = response.data
        for event in returned_events:
            self.assertEqual(event['organization'], self.user.id)


class UpdateProfileViewTest(APITestCase):
    def setUp(self):
        self.attendee = EventNestUserFactory.create(role="attendee")
        self.url = reverse('attendee-profile-view')

    def test_get_attendee_profile(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " +
            get_access_token(self.attendee)["access"]
        )
        response = self.client.get(self.url, format="json")
        self.assertIn("name", response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_not_registered_attendee_profile(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, 401)

    def test_update_attendee_profile(self):
        data = {
            "name": "Updated name",
            "email": "email@gmail.com"
        }
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " +
            get_access_token(self.attendee)["access"]
        )
        response = self.client.put(self.url, data=data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.data)
        self.assertIn("email", response.data)

    def test_update_attendee_profile_with_invalid_email(self):
        data = {
            "name": 'updated name',
            "email": "email"
        }
        data2 = {
            "name": 123123,
            "email": "email@gmail"
        }
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " +
            get_access_token(self.attendee)["access"]
        )

        response = self.client.put(self.url, data=data, format="json")
        response2 = self.client.put(self.url, data=data2, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response2.status_code, 400)
        self.assertIn("error", response.data)
        self.assertIn("error", response2.data)

    def test_update_attendee_with_empty_fields(self):
        data = {
            "name": "",
            "email": ""
        }
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " +
            get_access_token(self.attendee)["access"]
        )

        response = self.client.put(self.url, data=data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)


class GiveRatingTest(APITestCase):
    def setUp(self):
        self.event = EventsFactory.create()
        self.url = reverse("rating-view", kwargs={'pk': self.event.id})
        self.attendee = EventNestUserFactory.create(role="attendee")
        self.attendee_event = AttendeeEventFactory.create(
            Attendee=self.attendee,
            event=self.event
            )

    def test_post_rating_with_valid_data(self):
        data = {'rating': 5}
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " +
            get_access_token(self.attendee)["access"]
        )
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, 200)
        prev_rating = self.event.rating
        new_rating = (prev_rating + data['rating'])/2
        self.assertEqual(response.data['rating'], new_rating)

    def test_boundary_value_for_rating(self):
        data = {'rating': 6}
        data2 = {'rating': 0}
        self.client.credentials(HTTP_AUTHORIZATION=(
            "Bearer "+get_access_token(self.attendee)["access"]
        ))
        response = self.client.post(self.url, data=data, format="json")
        response2 = self.client.post(self.url, data=data2, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response2.status_code, 400)
        self.assertIn("error", response.data)
        self.assertIn("error", response2.data)
