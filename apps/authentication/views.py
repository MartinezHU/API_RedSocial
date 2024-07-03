from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.authentication.schemas import UserRegistrationResponseSchema
from apps.authentication.serializers import UserRegistrationSerializer
from apps.users.models import CustomUser


# Create your views here.
class UserRegistrationViewSet(ModelViewSet):
    queryset = CustomUser.objects.none()
    serializer_class = UserRegistrationSerializer
    http_method_names = ['post']
    permission_classes = [AllowAny]

    @extend_schema(
        responses={
            201: UserRegistrationResponseSchema
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response({"message": "Usuario creado exitosamente."}, status=status.HTTP_201_CREATED, headers=headers)


class MyTokenObtainPairView(TokenObtainPairView):
    pass


class MyTokenRefreshView(TokenRefreshView):
    pass
