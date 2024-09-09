from django.conf import settings
from rest_framework import serializers

from apps.users.models import CustomUser


class UserBasicSerializer(serializers.ModelSerializer):
    profile_pic_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'uuid',
            'username',
            'profile_pic_url'
        ]

    def get_profile_pic_url(self, obj):
        # Construye la URL completa usando el host del sitio
        request = self.context.get('request')  # Obtén el request del contexto
        if obj.profile_pic:
            url = f"http://192.168.1.27:8000{obj.profile_pic.url}"  # Construye la URL completa
            return url
        return None


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username',
        ]


class UserSerializer(serializers.ModelSerializer):
    # followers = serializers.SerializerMethodField();
    # followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    followers = FollowerSerializer(many=True, read_only=True)
    following = FollowerSerializer(many=True, read_only=True)

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
            'cover_photo',
            'bio',
            'date_of_birth',
            'location',
            'website',
            'mail_notifications',
            'gender',
            'is_private',
            'is_verified',
            'is_online',
            'followers',
            'following'
        ]
        ordering = ['id']

    # def get_followers(self, obj):
    #     request = self.context.get('request', None)
    #     max_depth = 2
    #     return self.serialize_followers(obj.followers.all(), current_depth=1, max_depth=max_depth)
    #
    # def serialize_followers(self, followers, current_depth, max_depth):
    #     if current_depth > max_depth:
    #         return []
    #
    #     return [
    #         {
    #             'uuid': follower.uuid,
    #             'username': follower.username,
    #             'email': follower.email,
    #             'followers': self.serialize_followers(follower.followers.all(), current_depth + 1, max_depth)
    #         }
    #         for follower in followers
    #     ]
