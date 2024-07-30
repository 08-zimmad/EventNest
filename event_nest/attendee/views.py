from authentication.jwt_authentication_class import CustomJWTAuthentication
from authentication.permissions import AttendeePermission
from django.conf import settings
from django.shortcuts import get_object_or_404
from organizer.models import EventNestUsers, Events, count_registered_attendees
from organizer.serializer import EventNestUserSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import AttendeeEvent, EmailTemplate
from .serializers import (
    AttendeeProfileSerializer,
    AttendeeRegisterToEventSerializer,
    GetEventSerializer,
    RatingSerializer
    )
from .utils.email import send_email_to_attendee


class AttendeeRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        data.update({"organization": None})
        serializer = EventNestUserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                },
                status=status.HTTP_201_CREATED
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventView(APIView):
    permission_classes = [AttendeePermission]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request, pk):
        events = get_object_or_404(Events, id=pk)
        serializer = GetEventSerializer(events)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        event = get_object_or_404(Events, id=pk)
        attendee = EventNestUsers.objects.get(email=request.user)
        attendee_event, created = AttendeeEvent.objects.get_or_create(
            Attendee=attendee,
            event=event
            )
        count_registered_attendees(events=event.id)
        if created:
            email = EmailTemplate.objects.all().first()
            subject = email.subject
            body = email.template
            from_email = settings.EMAIL_HOST_USER
            recipient_list = str(request.user)
            AttendeeRegisterToEventSerializer(data=attendee_event)
            send_email_to_attendee(subject, body, from_email, recipient_list)
            return Response(
                {
                    'data': "Registered Successfully"
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'data': "Already Registered"
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def delete(self, request, pk):
        get_object_or_404(Events, id=pk)
        data = AttendeeEvent.objects.filter(
            Attendee__email=request.user,
            event__id=pk
            ).prefetch_related('Attendee', 'event')
        self.check_object_permissions(request, data)

        if data.exists():
            data.delete()
            return Response(
                {
                    'success': "Successfully deleted"
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'error': "Selected Entry does not exists"
            },
            status=status.HTTP_404_NOT_FOUND
        )


class FetchAllEventsViews(APIView):
    permission_classes = [AttendeePermission]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        events = Events.objects.all()

        if events is not None:
            serializer = GetEventSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class UpdateProfileView(APIView):
    permission_classes = [AttendeePermission]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        user = get_object_or_404(EventNestUsers, email=request.user)
        serializer = AttendeeProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = get_object_or_404(EventNestUsers, email=request.user)
        data = request.data

        serializer = AttendeeProfileSerializer(user, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {
                'error': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class GiveRating(APIView):
    permission_classes = [AttendeePermission]
    authentication_classes = [CustomJWTAuthentication]

    def post(self, request, pk):
        user = request.user
        event = get_object_or_404(Events, id=pk)
        try:
            AttendeeEvent.objects.get(Attendee=user, event=event)
        except AttendeeEvent.DoesNotExist:
            return Response(
                {
                    "error": "You are not registered to the event"
                },
                status=status.HTTP_400_BAD_REQUEST)
        if event.rating == 0:
            rating = request.data['rating']
        elif request.data['rating'] <= 0 or request.data['rating'] > 5:
            return Response(
                {
                    "error": "Rating should be 1 to 5"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            rating = (event.rating + request.data['rating'])/2

        serializer = RatingSerializer(event, data={'rating': rating})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
