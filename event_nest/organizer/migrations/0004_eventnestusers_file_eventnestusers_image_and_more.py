# Generated by Django 5.0.6 on 2024-07-01 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0003_alter_eventnestusers_organization_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventnestusers',
            name='file',
            field=models.FileField(null=True, upload_to='file/'),
        ),
        migrations.AddField(
            model_name='eventnestusers',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='eventnestusers',
            name='video',
            field=models.FileField(null=True, upload_to='videos/'),
        ),
    ]