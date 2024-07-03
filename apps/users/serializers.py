from rest_framework import serializers

from apps.users.models import CustomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            # 'id',
            'uuid',
            'username',
            'email',
            'date_joined',
            'is_staff',
            'profile_pic',
        ]
        ordering = ['id']
