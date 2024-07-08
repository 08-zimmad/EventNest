from rest_framework import serializers
from organizer.models import Events, EventNestUsers
from .models import AttendeeEvent


class AttendeeSerializer(serializers.ModelSerializer):

    class Meta:
        model=Events
        fields=['title','description','date','time','duration','venue_details']


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model= EventNestUsers
        fields = [ 'name','email']


class AttendeeRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model=AttendeeEvent
        fields="__all__"


class AttendeeProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventNestUsers
        fields = [ 'name']


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Events
        fields = ['rating']
