import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


def user_profile_pic_path(instance, filename):
    # Generar UUID basado en el username del usuario
    uuid_filename = f'{instance.username}_{uuid.uuid4()}'
    ext = filename.split('.')[-1]  # Obtener extensión del archivo
    return f'profile_pics/{uuid_filename}.{ext}'  # Ruta de almacenamiento


class CustomUser(AbstractUser):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    profile_pic = models.ImageField(upload_to=user_profile_pic_path, null=True, blank=True,
                                    default='/default/default_profile_pic.svg')

    def __str__(self):
        return self.username
