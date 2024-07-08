from smtplib import SMTPConnectError, SMTPServerDisconnected

from authentication.jwt_authentication_class import CustomJWTAuthentication
from authentication.permissions import AttendeePermission
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from organizer.models import EventNestUsers, Events, register_attendee
from organizer.serializer import EventNestUserSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import AttendeeEvent, EmailTemplate
from .serializers import (AttendeeProfileSerializer,
                          AttendeeRegistrationSerializer, AttendeeSerializer,
                          RatingSerializer)


class AttendeeRegistration(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        data.update({"organization":None})
        serializer = EventNestUserSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            status = status.HTTP_201_CREATED
            )

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class EventRegistration(APIView):
    permission_classes = [AttendeePermission]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request, pk):
        events=get_object_or_404(Events, id=pk)
        serializer=AttendeeSerializer(events)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request,pk):
        event=get_object_or_404(Events, id=pk)
        attendee = EventNestUsers.objects.get(email=request.user)
        if register_attendee(events=event.id):
            attendee_event, created=AttendeeEvent.objects.get_or_create(
                Attendee=attendee,
                event=event
                )
        else:
            Response(
                {
                    "error":"Some error occured. Try registring again"
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        if created is True:
            email = EmailTemplate.objects.values('subject','template')
            subject = email[0]['subject']
            body = email[0]['template']
            from_email = settings.EMAIL_HOST_USER
            recipient_list= [request.user]

            try:
                send_mail(
                    subject,
                    body,
                    from_email,
                    recipient_list
                    )
                AttendeeRegistrationSerializer(data=attendee_event)
            except SMTPConnectError:
                return Response(
                    {
                        "error":"Server Connection Error"
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except SMTPServerDisconnected:
                return Response(
                    {
                        "error":"Server Connection Error"
                    },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(
                {
                    'data':"Registered Successfully"
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'data':"Already Registered"
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def delete(self, request, pk):
        get_object_or_404(Events, id=pk)
        data=AttendeeEvent.objects.filter(
            Attendee__email=request.user,
            event__id=pk
            ).prefetch_related('Attendee', 'event')

        self.check_object_permissions(request,data)

        if not data.exists():
            return Response({'error':"Selected Entry does not exists"})

        data.delete()
        return Response(
            {
                'success':"Successfully deleted"
            },
            status=status.HTTP_200_OK
        )


class FetchAllEventsViews(APIView):
    permission_classes = [AttendeePermission]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        events=Events.objects.all()

        if events is not None:
            serializer=AttendeeSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_200_OK)


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
            return  Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {
                'error':serializer.errors
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
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            rating = (event.rating + request.data['rating'])/2

        serializer = RatingSerializer(event,data={'rating':rating})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
