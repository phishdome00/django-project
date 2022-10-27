from rest_framework import serializers
from .models import Violation


class ViolationListSerializer(serializers.ModelSerializer):

    class Meta:
        model=Violation
        fields='__all__'


class ViolationCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model=Violation
        fields=('id', 'url', 'displayed_url', 'description', 'extra_info', 'position', 'title', 'app', 'query', 'violator_url',
        'date', 'status')
