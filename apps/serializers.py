from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import App
from user_profile.serializers import UserLoginSerializer

class AppSerializer(serializers.ModelSerializer):

    class Meta:
        model=App
        fields=('id', 'appname', 'appurl', 'user')


class AppListSerializer(serializers.ModelSerializer):
    user=UserLoginSerializer()
    class Meta:
        model=App
        fields=('id', 'appname', 'appurl', 'user')