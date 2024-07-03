from apps.core.views import BaseViewSet
from apps.users.models import CustomUser
from apps.users.permissions import IsOwnerOrStaffOrReadOnly, IsStaffPermission
from apps.users.serializers import UserSerializer


# Create your views here.


class UserView(BaseViewSet):
    permission_classes = [IsOwnerOrStaffOrReadOnly, IsStaffPermission]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uuid'
    search_fields = ['username']
    ordering_fields = ['id', 'username', 'date_joined']
    http_method_names = ['get', 'put', 'patch', 'delete', 'head', 'options']
