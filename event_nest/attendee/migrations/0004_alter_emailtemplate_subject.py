# Generated by Django 5.0.6 on 2024-06-26 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0003_emailtemplate_created_at_emailtemplate_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='subject',
            field=models.CharField(max_length=60),
        ),
    ]