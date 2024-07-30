from rest_framework import serializers
from organizer.models import Events, EventNestUsers
from .models import AttendeeEvent


class GetEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Events
        fields = [
            'title',
            'description',
            'date',
            'time',
            'duration',
            'venue_details',
            'organization'
            ]
        read_only_fields = fields


class AttendeeRegisterToEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttendeeEvent
        fields = "__all__"


class AttendeeProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventNestUsers
        fields = ['name', 'email']

    def validate(self, attrs):
        if 'name' in attrs:
            if not isinstance(attrs['name'], str):
                raise serializers.ValidationError("Name should not numbers")

        if 'email' in attrs:
            if not attrs['email']:
                raise serializers.ValidationError(
                    "Email field cannot be empty"
                    )
            if not serializers.EmailField().to_internal_value(attrs['email']):
                raise serializers.ValidationError(
                    "Invalid email format"
                    )
        return attrs


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Events
        fields = ['rating']
