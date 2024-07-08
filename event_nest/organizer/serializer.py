from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.utils.timezone import now
from .models import EventNestUsers,Events



class EventNestUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventNestUsers
        fields = [ 'name','email', 'password', 'is_active', 'is_staff',"organization", "role"]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        user = EventNestUsers.objects.create(**validated_data)
        return user


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
        return attr


class OrganizerSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventNestUsers
        fields = [ 'name','email',"organization"]


class OrganizerAttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Events
        fields = ['present_count']

    # def get_formatted_rating(self,obj):
    #     return format(obj.rating, '.2f')


class EventMediaFilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Events
        fields = ['image', 'video', 'file']


class GetAttendeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventNestUsers
        fields = ['email','name']
