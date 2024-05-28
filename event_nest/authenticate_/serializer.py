from rest_framework import serializers
from .models import Organizer
from django.contrib.auth import get_user_model


Organizer = get_user_model()

class OrganizerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)




class OrganizerSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Organizer
        fields = [ 'email','password']

    def create(self, validated_data):
        user = Organizer.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
