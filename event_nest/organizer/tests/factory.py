from datetime import datetime, timedelta

import factory
from faker import Faker

from ..models import EventNestUsers, Events


class EventNestUserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = EventNestUsers

    name = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall(
        'set_password',
        'defaultpassword')
    organization = factory.Faker("company")
    role = factory.Iterator(["organizer", "attendee"])


fake = Faker()


class EventsFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Events

    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("text")
    date = factory.LazyFunction(
        lambda: fake.date_between(start_date='today', end_date='+30y'))
    organization = factory.SubFactory(EventNestUserFactory)
    duration = factory.LazyFunction(lambda: timedelta(hours=2))
    venue_details = factory.Faker('url')
    registration_count = factory.Faker('pyint', min_value=0, max_value=100)
    present_count = factory.Faker('pyint', min_value=0, max_value=100)
    image = factory.django.ImageField(color='blue')
    video = factory.django.FileField(filename="text.mp4")
    file = factory.django.FileField(filename='the_file.dat')
    rating = factory.Faker('pyfloat', left_digits=1,
                           right_digits=2, min_value=0,
                           max_value=5)

    @factory.lazy_attribute
    def time(self):
        now = datetime.now()
        time = now + timedelta(hours=1)
        return time.time()
