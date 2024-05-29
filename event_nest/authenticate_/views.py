from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .models import Organizer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import OrganizerSerializer

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



