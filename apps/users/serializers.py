from django.contrib.auth.models import User
from rest_framework import serializers


class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'url',
            'id',
            'username',
            'email',
            'date_joined',
            'is_staff',
        ]
        ordering = ['id']
