from django.shortcuts import render,HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from .serializer import OrganizerLoginSerializer, OrganizerSignupSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import Organizer
from django.contrib.auth import authenticate
# Create your views here.



class OrganizerLogin(APIView):
    def post(self, request):
        data = request.data
        serializer = OrganizerLoginSerializer(data=data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(email=email, password=password)
            if user is None:
                return Response({"message": "Wrong credentials"}, status=status.HTTP_400_BAD_REQUEST)
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




class SignUpView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OrganizerSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
