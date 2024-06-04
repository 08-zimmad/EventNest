from rest_framework.views import APIView
# from rest_framework.authentication import J
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoObjectPermissions
from django.contrib.auth import authenticate
from .models import Organizer,Events
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import OrganizerSerializer, EventsSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .authenticate import CustomJWTAuthentication

from django.contrib.auth import get_user_model
User = get_user_model()

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




class OrganizerLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request,email=email, password=password)
        if user:
            refresh=RefreshToken.for_user(user)
            return Response({
                'refresh':str(refresh),
                'access':str(refresh.access_token),
            },status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


class EventView(APIView):
    permission_classes = [IsAuthenticated,DjangoObjectPermissions]
    authentication_classes=[CustomJWTAuthentication]
    queryset = Organizer.objects.all()



    def get_object(self,id):
        try:
            return Events.objects.get(id=id)
        except Events.DoesNotExist:
            return None
        


    def get(self,request):
            organizer=Organizer.objects.prefetch_related('events_set').get(email=request.user)
            events=organizer.events_set.all()
            if events.exists():
                serializer=EventsSerializer(events,many=True)
                return Response({'data':serializer.data},status=status.HTTP_200_OK)
            return Response({'data':{}}, status=status.HTTP_204_NO_CONTENT)
        
# implement try and except here
        
    def post(self, request):
        serializer=EventsSerializer(data=request.data)
        if serializer.is_valid():
            organizer = Organizer.objects.get(email=request.user)
            serializer.save(organization=organizer)
            return Response({'Success':"Event Created Successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request, id):
        event=self.get_object(id)
        if event is None:
            return Response({'error':'Event Not Found'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request,event)
        serializer=EventsSerializer(event,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        