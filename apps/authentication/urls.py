from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.authentication.views import UserRegistrationViewSet, MyTokenObtainPairView, MyTokenRefreshView

router = SimpleRouter()

router.register(r'signup', UserRegistrationViewSet, basename='user')

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
