from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from rest_framework import serializers

from .models import EventNestUsers, Events

class EventNestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventNestUsers
        fields = ['name', 'email', 'password', 'organization', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True},
        }

    def validate(self, attrs):
        if ('name' in attrs and 
            not isinstance(attrs["name"], str)):
                raise serializers.ValidationError("Name should not be integers")

        if 'email' in attrs:
            if not attrs['email']:
                raise serializers.ValidationError("Email field cannot be empty")
            if not serializers.EmailField().to_internal_value(attrs['email']):
                raise serializers.ValidationError("Invalid email format")

        if 'role' in attrs:
            valid_roles = ['attendee', 'organizer']
            if attrs['role'].lower() not in valid_roles:
                raise serializers.ValidationError("Role should be either 'attendee' or 'organizer'")

        return attrs


    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        user = EventNestUsers.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.password = make_password(password)
        instance.save()
        return instance


class EventNestUserOauthSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventNestUsers
        fields = [ 'name','email']
    def create(self, validated_data):
        user = EventNestUsers.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password'],
            organization=validated_data['organization']
        )
        return user


class EventsSerializer(serializers.ModelSerializer):

    class Meta:
        model=Events
        fields=['title','description','date','time','duration','venue_details']

    def validate(self, attr):
        event_date = attr['date']
        event_time = attr['time']
        title = attr['title']
        description = attr['description']
        venue_details = attr['venue_details']
        

        date_time_now = now()
        current_date = date_time_now.date()
        current_time = date_time_now.time()

        if (event_date < current_date):
            raise serializers.ValidationError(
                "Date cannot be in past"
            )
        elif (event_date == current_date and
              event_time <= current_time):
            raise serializers.ValidationError("Time cannot be in past")
        
        if not isinstance(title, str):
            raise serializers.ValidationError("Title must be a string")
        
        if not isinstance(description, str):
            raise serializers.ValidationError("description must be a string")

        if not isinstance(venue_details, str):
            raise serializers.ValidationError("venue_details must be a string")

        return attr


class OrganizerSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventNestUsers
        fields = [ 'name','email',"organization"]



class OrganizerAttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Events
        fields = ['present_count']

    def validate(self, attr):
        present_count = attr['present_count']
        if not isinstance(present_count, int):
            raise serializers.ValidationError("Use Integer Values")

        return attr


class EventMediaFilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Events
        fields = ['image', 'video', 'file']


class GetAttendeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventNestUsers
        fields = ['email','name']
