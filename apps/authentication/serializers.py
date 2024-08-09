import json
import re
import string

from django import db
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import CustomUser


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.username
        if user.profile_pic:
            token['profile_img'] = 'http://localhost:8000' + user.profile_pic.url
        # token['email'] = user.email
        return token


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password_confirm', 'email']

    def validate(self, attrs):
        email = attrs.get("email")
        password1 = attrs.get('password')
        password2 = attrs.get('password_confirm')
        username = attrs.get('username')

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': "El email ya está en uso."})

        self.validate_username(username)
        self.validate_password(password1)

        if password1 != password2:
            raise serializers.ValidationError({'password': "Las contraseñas no coinciden."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')  # Eliminar password_confirm ya que no es necesario para crear el usuario
        with db.transaction.atomic():
            user = CustomUser.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
        return user

    @staticmethod
    def validate_username(value):
        if not re.match(r'^[a-zA-Z0-9_.-]{5,16}$', value):
            raise serializers.ValidationError(
                "El nombre de usuario debe contener entre 5 y 16 caracteres y solo puede incluir letras, números, "
                "guiones bajos, puntos y guiones.")
        return value

    @staticmethod
    def validate_password(value):
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("La contraseña debe contener al menos una letra minúscula.")
        if not any(char in string.punctuation for char in value):
            raise serializers.ValidationError("La contraseña debe contener al menos un signo de puntuación.")
        return value
