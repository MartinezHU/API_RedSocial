from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.core.views import BaseViewSet
from apps.posts.models import Post, PostImage, Comment, Dislike, Like, Reaction
from apps.posts.permissions import IsAuthenticatedForActions
from apps.posts.serializers import PostSerializer, PostImageSerializer, CommentSerializer
from apps.users.permissions import IsOwnerOrStaffOrReadOnly


# Create your views here.


class PostView(BaseViewSet):
    permission_classes = [AllowAny, IsAuthenticatedForActions]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['post'], url_path='interact')
    def interact(self, request):
        post = self.get_object()
        action_type = request.data.get('action')
        user = request.user

        if action_type == 'like':
            Dislike.objects.filter(user=user, post=post).delete()
            Like.objects.get_or_create(user=user, post=post)
            post.likes_count = post.likes_count + 1
            post.save()
            return Response({'status': 'Post liked'}, status=status.HTTP_200_OK)
        elif action_type == 'dislike':
            Like.objects.filter(user=user, post=post).delete()
            Dislike.objects.get_or_create(user=user, post=post)
            post.dislikes_count = post.dislikes_count + 1
            post.save()
            return Response({'status': 'Post disliked'}, status=status.HTTP_200_OK)

        return Response({'error': 'Acción no válida'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='react')
    def react(self, request):
        post = self.get_object()
        user = request.user
        reaction_type = request.data.get('reaction')

        # Obtener las opciones válidas desde el modelo Reaction
        valid_reactions = dict(Reaction.EMOJI_CHOICES).keys()

        # Validar que la reacción sea válida
        if reaction_type not in valid_reactions:
            return Response({'error': 'Reacción no válida'}, status=status.HTTP_400_BAD_REQUEST)

        # Buscar si el usuario ya ha reaccionado a este post
        reaction, created = Reaction.objects.get_or_create(user=user, post=post).delete()

        if created:
            # Si no existía ninguna reacción, se ha creado una nueva
            reaction.reaction = reaction_type
            reaction.save()
            return Response({'status': f'Post reacted with {reaction_type}'}, status=status.HTTP_201_CREATED)
        else:
            # Si ya existía una reacción, simplemente actualizamos el tipo de reacción
            if reaction.reaction != reaction_type:
                reaction.reaction = reaction_type
                reaction.save()
                return Response({'status': f'Reaction updated to {reaction_type}'}, status=status.HTTP_200_OK)
            else:
                # Si la reacción es la misma, no hay necesidad de hacer nada
                return Response({'status': 'Reaction is already set to this type'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='add-comment')
    def add_comment(self, request, pk=None):
        post = self.get_object()
        comment_serializer = CommentSerializer(data=request.data)
        if comment_serializer.is_valid():
            comment_serializer.save(post=post, user=request.user)
            return Response(comment_serializer.data, status=status.HTTP_201_CREATED)

        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='remove-comment/(?P<comment_id>\d+)')
    def remove_comment(self, request, pk=None, comment_id=None):
        post = self.get_object()
        try:
            comment = Comment.objects.get(post=post, id=comment_id)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='add-image')
    def add_image(self, request, pk=None):
        post = self.get_object()
        serializer = PostImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def remove_image(self, request, pk=None, image_id=None):
        post = self.get_object()
        try:
            image = PostImage.objects.get(post=post, id=image_id)
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PostImage.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)


class RecommendedFeedView(BaseViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    http_method_names = ['get']

    # def list(self, request, *args, **kwargs):
    #     posts = Post.objects.all()
    #     serializer = PostSerializer(posts, many=True)
    #     return Response(serializer.data)


class MyPostsFeedView(BaseViewSet):
    # queryset = Post.objects.filter()
    # serializer_class = PostSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        posts = Post.objects.filter(user=request.user)
        serializer = PostSerializer(posts, many=True)
        Response(serializer.data)
