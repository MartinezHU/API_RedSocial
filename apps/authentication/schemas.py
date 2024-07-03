from rest_framework.serializers import Serializer, CharField, IntegerField


class UserRegistrationResponseSchema(Serializer):
    message = CharField(default='Usuario registrado correctamente')
    status = IntegerField(default=201)
