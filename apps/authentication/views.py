from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.authentication.serializers import UserRegistrationSerializer


# Create your views here.
@extend_schema(tags=['Authentication'])
class UserRegistrationViewSet(ModelViewSet):
    queryset = User.objects.none()
    serializer_class = UserRegistrationSerializer
    http_method_names = ['post']


@extend_schema(tags=['Authentication'])
class MyTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(tags=['Authentication'])
class MyTokenRefreshView(TokenRefreshView):
    pass
