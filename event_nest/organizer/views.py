from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Organizer,Events
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import OrganizerSerializer, EventsSerializer
from .authentication_class import CustomJWTAuthentication
# from .permissions import isOrganizer
from .permissions import CustomModelPermission
from django.shortcuts import get_object_or_404
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework.exceptions import AuthenticationFailed


class OrganizerRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer=OrganizerSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            refresh=RefreshToken.for_user(user)
            return Response({
                'refresh':str(refresh),
                'access':str(refresh.access_token),
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class EventView(APIView):
    permission_classes = [CustomModelPermission]
    authentication_classes=[CustomJWTAuthentication]



        


    def get(self,request):
        try:
            organizer=Organizer.objects.prefetch_related('events_set').get(email=request.user)
        except Organizer.DoesNotExist:
            raise AuthenticationFailed("Organizer Not Authenticated")
        events=organizer.events_set.all()
        if events.exists():
            serializer=EventsSerializer(events,many=True)
            return Response({'data':serializer.data},status=status.HTTP_200_OK)
        return Response({'data':{}}, status=status.HTTP_204_NO_CONTENT)
        
# implement try and except here
        
    def post(self, request):
        serializer=EventsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                organizer = Organizer.objects.get(email=request.user)
            except Organizer.DoesNotExist:
                raise AuthenticationFailed("Organizer Not Authenticated")
            serializer.save(organization=organizer)
            return Response({'Success':"Event Created Successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


    def put(self, request, event_id):
        event=get_object_or_404(Events,id=event_id)
        self.check_object_permissions(request,event)
        serializer=EventsSerializer(event,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_304_NOT_MODIFIED)

    

    def patch(self, request, event_id):
        event=Events.objects.get(id=event_id)
        serializer=EventsSerializer(event,request.data, partial=True)
        if serializer.is_valid():
            return Response({'success':'Partially Updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)


    def delete(self,request,event_id):
        event=get_object_or_404(Events,id=event_id)
        self.check_object_permissions(request,event)
        if event is event.exists():
            return Response({"error":"Event Not Found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success':"Successfully Deleted"}, status=status.HTTP_200_OK)
    






# views.py

from django.shortcuts import render

def google_login(request):
    return render(request, 'google_login.html')
