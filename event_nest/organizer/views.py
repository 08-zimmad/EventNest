from rest_framework_simplejwt.tokens import RefreshToken
from authentication.jwt_authentication_class import CustomJWTAuthentication
from authentication.permissions import OrganizerPermission
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from attendee.models import AttendeeEvent
from .models import EventNestUsers
from .models import Events
from .serializer import (EventNestUserSerializer, EventsSerializer,
                         OrganizerSerializer, OrganizerAttendanceSerializer,
                         EventMediaFilesSerializer, GetAttendeeSerializer
                        )


class EventNestRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EventNestUserSerializer(data=request.data)

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


class GetEventView(APIView):
    permission_classes = [OrganizerPermission]
    authentication_classes=[CustomJWTAuthentication]

    def get(self, request, pk):
        event=get_object_or_404(Events, id=pk)
        self.check_object_permissions(request, event)
        serializer = EventsSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventView(APIView):
    permission_classes = [OrganizerPermission]
    authentication_classes=[CustomJWTAuthentication]

    def get(self,request):
        user = EventNestUsers.objects.get(email = request.user)
        events = Events.objects.prefetch_related().filter(organization = user)

        if events.exists():
            serializer=EventsSerializer(events, many = True)
            return Response(serializer.data,status = status.HTTP_200_OK)

        return Response(
            {
                'error': 'No Event Exists'
            },
            status= status.HTTP_204_NO_CONTENT
        )

    def post(self, request):
        serializer = EventsSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = EventNestUsers.objects.get(email=request.user)

            except EventNestUsers.DoesNotExist:
                return Response(
                    {
                        "error": "User is not authenticated"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            serializer.save(organization=user)
            return Response(
                {
                    'Success': "Event Created Successfully"
                },
                    status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, event_id):
        event = get_object_or_404(Events, id=event_id)
        self.check_object_permissions(request, event)

        serializer = EventsSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, event_id):
        event = get_object_or_404(Events, id=event_id)
        self.check_object_permissions(request, event)

        serializer = EventsSerializer(event, request.data, partial=True)

        if serializer.is_valid():
            return Response(
                {
                    'success':'Partially Updated'
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, event_id):
        event = get_object_or_404(Events, id=event_id)
        self.check_object_permissions(request, event)
        event.delete()
        return Response(
            {
                'success':"Successfully Deleted"
            },
                status=status.HTTP_200_OK
        )


class UpdateProfileView(APIView):
    permission_classes = [OrganizerPermission]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        user = get_object_or_404(EventNestUsers, email=request.user)
        serializer = OrganizerSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = get_object_or_404(EventNestUsers, email=request.user)
        data = request.data

        serializer = OrganizerSerializer(user,data=data)

        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {
                'error':serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class MarkAttendanceView(APIView):
    permission_classes = [OrganizerPermission]
    authentication_classes = [CustomJWTAuthentication]
    def post(self, request, pk):
        event=get_object_or_404(Events, id=pk)
        self.check_object_permissions(request, event)
        if event.registration_count < request.data['present_count']:
            return Response(
                {'error': "Attendance count is greater than registered attendees"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OrganizerAttendanceSerializer(event, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadMediaFilesView(APIView):
    permission_classes = [OrganizerPermission]
    authentication_classes = [CustomJWTAuthentication]

    def post(self, request, pk):
        event = get_object_or_404(Events, id=pk)
        self.check_object_permissions(request,event)

        serializer = EventMediaFilesSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAttendeeRegistrationView(APIView):
    permission_classes = [OrganizerPermission]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request, pk):
        event=get_object_or_404(Events, id=pk)
        self.check_object_permissions(request, event)
        attendees_events = AttendeeEvent.objects.filter(event=event).select_related('Attendee')
        attendees = [attendee_event.Attendee for attendee_event in attendees_events]
        serializer = GetAttendeeSerializer(attendees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def google_login(request):
    return render(request, 'google_login.html')
