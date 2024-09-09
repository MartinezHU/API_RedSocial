from email.policy import default

from django.core.exceptions import ValidationError
from django.db import models

from apps.users.models import CustomUser


# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()  # El contenido textual de la publicación
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_count = models.PositiveIntegerField(default=0)
    dislikes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content[:50]  # Muestra solo los primeros 50 caracteres


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Permite modificar los likes

    def clean(self):
        super().clean()
        if Dislike.objects.filter(user=self.user, post=self.post).exists():
            raise ValidationError("No puedes dar 'Like' si ya has dado 'Dislike' a este post.")


class Dislike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    disliked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Permite modificar los dislikes

    def clean(self):
        super().clean()
        if Like.objects.filter(user=self.user, post=self.post).exists():
            raise ValidationError("No puedes dar 'Dislike' si ya has dado 'Like' a este post.")


class Reaction(models.Model):
    EMOJI_CHOICES = [
        ('like', '👍'),
        ('love', '❤️'),
        ('haha', '😂'),
        ('wow', '😮'),
        ('sad', '😢'),
        ('angry', '😡'),
        ('clap', '👏'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=10, choices=EMOJI_CHOICES)
    reacted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} reacted {self.reaction} to post {self.post.id}"

    def clean(self):
        super().clean()
        if Reaction.objects.filter(user=self.user, post=self.post).exists():
            raise ValidationError("Ya has reaccionado a este post.")


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for post {self.post.id}"

    def clean(self):
        super().clean()
        # Verifica si la instancia de PostImage ya existe en la base de datos
        if self.pk is None:  # Es una nueva instancia
            # Verificar el número de imágenes asociadas al post
            num_imagenes = PostImage.objects.filter(post=self.post).count()
            if num_imagenes >= 4:
                raise ValidationError('Un post no puede tener más de 4 imágenes.')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:50]  # Muestra solo los primeros 50 caracteres

    def clean(self):
        super().clean()
        if self.content is None:
            raise ValidationError('El contenido del post no pueda estar vacío.')


class SharePost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shares')
    shared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} shared post {self.post.id}"
