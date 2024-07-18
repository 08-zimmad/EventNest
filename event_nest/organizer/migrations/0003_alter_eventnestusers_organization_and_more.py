# Generated by Django 5.0.6 on 2024-06-13 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0002_eventnestusers_events_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventnestusers',
            name='organization',
            field=models.CharField(max_length=40, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='events',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
        ),
    ]