# Generated by Django 4.1.2 on 2022-10-18 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='otp_send_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
