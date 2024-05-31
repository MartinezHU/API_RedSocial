from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from rest_framework import filters

from apps.core.base_views import BaseViewSet
from apps.users.serializers import UsuarioSerializer


# Create your views here.


@extend_schema(tags=['Users'])
class UsuarioView(BaseViewSet):
    # permission_classes = [IsOwnerOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username']
    ordering_fields = ['id', 'username', 'date_joined']
