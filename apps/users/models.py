import uuid

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


def user_profile_pic_path(instance, filename):
    # Generar UUID basado en el username del usuario
    uuid_filename = f'{instance.username}_{uuid.uuid4()}'
    ext = filename.split('.')[-1]  # Obtener extensión del archivo
    return f'profile_pics/{uuid_filename}.{ext}'  # Ruta de almacenamiento


class CustomUser(AbstractUser):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    profile_pic = models.ImageField(upload_to=user_profile_pic_path, null=True, blank=True,
                                    default='/default/default_profile_photo.jpg')
    cover_photo = models.ImageField(upload_to='cover_photos/', null=True, blank=True,
                                    default='/default/default_cover.jpg')
    bio = models.TextField(max_length=500, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    mail_notifications = models.BooleanField(default=True)
    gender = models.CharField(max_length=50, choices=[('M', 'Mujer'), ('H', 'Hombre'), ('O', 'Otro')], null=True,
                              blank=True)
    is_private = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following_set', blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers_set', blank=True)

    def __str__(self):
        return self.username

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         existing_user = CustomUser.objects.get(pk=self.pk)
    #         if self in existing_user.following.all() or self in existing_user.followers.all():
    #             raise ValidationError("No puedes seguirte a ti mismo.")
    #     super().save(*args, **kwargs)