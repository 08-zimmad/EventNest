from rest_framework import serializers
from .models import Organizer

class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = [ 'name','email', 'password', 'is_active', 'is_staff','organization']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True},
        }


# used for creating data instances in model
    def create(self, validated_data):
        user = Organizer.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password'],
            organization=validated_data['organization']
        )
        return user
