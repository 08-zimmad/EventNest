from unittest.mock import patch

from attendee.models import AttendeeEvent
from organizer.models import Events
from attendee.utils.token import get_access_token
from django.conf import settings
from django.urls import reverse
from organizer.tests.factory import EventNestUserFactory, EventsFactory
from rest_framework import status
from rest_framework.test import APITestCase

from .factory import AttendeeEventFactory, EmailTemplateFactory


class AttendeeRegistrationViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("attendee-signup-view")

        self.attendee_data = {
                "name":"Zimmad",
                "email":"fingerlicking@gmail.com",
                "password":"StrongPassword123",
                "role":"attendee",
                "organization":None
            }
    def test_attendee_falied_signup_post(self):
        invalid_data = self.attendee_data.copy()
        invalid_data["email"] = ""
        response = self.client.post(self.url, invalid_data, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn("email", response.data)

    def test_attendee_success_signup_post(self):
        response = self.client.post(self.url, self.attendee_data, format="json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)


class EventViewTest(APITestCase):

    def setUp(self):
        self.event = EventsFactory.create()
        self.user = EventNestUserFactory.create(role="attendee")
        self.attendee_event = AttendeeEventFactory(Attendee=self.user, event=self.event)
        self.email_template = EmailTemplateFactory.build()
        self.url = reverse("events-attendee-registration", kwargs={'pk':self.event.id})

    def test_get_specific_event_success_get(self):
        self.client.credentials(HTTP_AUTHORIZATION = (
            "Bearer "+get_access_token(self.user)['access']))
        response = self.client.get(self.url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn("title", response.data)
        self.assertIn("description", response.data)
        self.assertIn("date", response.data)
        self.assertIn("time", response.data)
        self.assertIn("duration", response.data)
        self.assertIn("venue_details", response.data)

    def test_get_specific_event_with_invalid_id_get(self):
        url = reverse("events-attendee-registration", kwargs={'pk':223})
        self.client.credentials(HTTP_AUTHORIZATION = (
            "Bearer "+get_access_token(self.user)['access']))
        response = self.client.get(url, format="json")
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertIn("detail", response.data)

    # @patch("attendee.utils.email.send_email_to_attendee")
    # def test_attendee_event_registration_success_post(self, mock_email):

    #     mock_email.return_value = None
    #     registration_data = {
    #         "Attendee":self.user.id,
    #         "event":self.event.id
    #     }
    #             self.client.credentials(HTTP_AUTHORIZATION = (
            # "Bearer "+get_access_token(self.user)['access']))
    #     response = self.client.post(self.url, registration_data, format="json")
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     mock_email.assert_called_once_with(self.email.body, self.email.template,
    #                                        settings.EMAIL_HOST_USER, self.user.email)

    def test_delete_event_success(self):
        self.client.credentials(HTTP_AUTHORIZATION = (
            "Bearer "+get_access_token(self.user)['access']))
        response = self.client.delete(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(AttendeeEvent.DoesNotExist):
            AttendeeEvent.objects.get(Attendee=self.user, event=self.event)


    def test_delete_event_with_invalid_id(self):
        url = reverse("events-attendee-registration", kwargs={'pk':1123})
        self.client.credentials(HTTP_AUTHORIZATION = (
            "Bearer "+get_access_token(self.user)['access']))
        response = self.client.delete(url, format="json")
        qs = AttendeeEvent.objects.filter(Attendee=self.user, event=self.event)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(qs.exists())


class FetchAllEventsViewsTest(APITestCase):

    def setUp(self):
        self.url = reverse("get-all-events-available-view")
        self.user = EventNestUserFactory.create(role="attendee")
        self.events = EventsFactory.create_batch(10, organization=self.user)
    
    def test_get_all_events_success(self):
        self.client.credentials(HTTP_AUTHORIZATION = (
            "Bearer "+get_access_token(self.user)['access']
        ))
        response = self.client.get(self.url, format="json")
        events = Events.objects.all().count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(events, 10)

    # def test_get_events_with_unauthenticated_user(self):
    #     response = self.client.get(self.url, format="json")
    #     self.assertEqual(response.status_code, 401)
    #     self.assertIn("detail", response.data)
    
    # def test_get_all_event_with_authorized_user(self):
    #     self.client.force_authenticate(self.user)
    #     response = self.client.get(self.url, format="json")
    #     self.assertEqual(response.status_code, 200)
    #     print(response.data)
    #     returned_events = response.data
    #     for event in returned_events:
    #         self.assertEqual(event['orgnization'], self.user.id)


# class 