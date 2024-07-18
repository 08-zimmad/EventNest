# Generated by Django 5.0.6 on 2024-07-03 08:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0011_alter_events_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5, validators=[django.core.validators.MaxValueValidator(5.0)]),
        ),
    ]