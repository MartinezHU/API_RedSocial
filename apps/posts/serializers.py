from rest_framework import serializers

from apps.posts.models import Post, PostImage, Comment, Like, Dislike, SharePost
from apps.users.models import CustomUser
from apps.users.serializers import UserSerializer, UserBasicSerializer


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = [
            'image',
        ]


class PostSerializer(serializers.ModelSerializer):
    user = serializers.UUIDField()  # Usamos UUIDField para aceptar el UUID del usuario
    images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'content',
            'created_at',
            'updated_at',
            'likes_count',
            'dislikes_count',
            'comments_count',
            'shares_count',
            'images',  # Agregamos el campo de imágenes
        ]

    def validate_user(self, value):
        # Aquí asumimos que `value` es el UUID
        if isinstance(value, dict):
            uuid = value.get('uuid')
        else:
            uuid = value

        if not CustomUser.objects.filter(uuid=uuid).exists():
            raise serializers.ValidationError("El usuario con este UUID no existe.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.get(uuid=validated_data.pop('user'))
        return Post.objects.create(user=user, **validated_data)

    def to_representation(self, instance):
        # Aquí se transforma la representación del post para incluir el usuario completo
        representation = super().to_representation(instance)
        representation['user'] = UserBasicSerializer(instance.user).data
        return representation


class LikeSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer()
    post = PostSerializer()

    class Meta:
        model = Like
        fields = [
            'user',
            'post',
            'liked_at',
            'updated_at',
        ]


class DislikeSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer()
    post = PostSerializer()

    class Meta:
        model = Like
        fields = [
            'user',
            'post',
            'disliked_at',
            'updated_at',
        ]


class ReactionSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer()
    post = PostSerializer()

    class Meta:
        model = Dislike
        fields = [
            'user',
            'post',
            'reaction',
            'reacted_at',
        ]


class CommentSerializer(serializers.ModelSerializer):
    # post = PostSerializer()
    user = UserBasicSerializer()

    class Meta:
        model = Comment
        fields = [
            'id',
            # 'post',
            'user',
            'content',
            'created_at',
            'updated_at'
        ]


class SharePostSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    user = UserBasicSerializer()

    class Meta:
        model = SharePost
        fields = [
            'user',
            'post',
            'shared_at'
        ]
