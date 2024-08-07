# Generated by Django 5.0.6 on 2024-08-05 12:28

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventNestUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('organization', models.CharField(max_length=40, null=True, unique=True)),
                ('role', models.CharField(choices=[('attendee', 'Attendee'), ('organizer', 'Organizer')], max_length=20, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, unique=True)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('duration', models.DurationField()),
                ('venue_details', models.TextField()),
                ('registration_count', models.PositiveIntegerField(default=0)),
                ('present_count', models.PositiveIntegerField(default=0)),
                ('image', models.ImageField(null=True, upload_to='image/')),
                ('video', models.FileField(null=True, upload_to='videos/')),
                ('file', models.FileField(null=True, upload_to='file/')),
                ('rating', models.FloatField(default=0.0, validators=[django.core.validators.MaxValueValidator(5.0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
