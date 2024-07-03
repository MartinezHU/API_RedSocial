from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.users.views import UserView

router = SimpleRouter()

router.register(r'usuario', UserView, basename="usuario")


urlpatterns = [
    path('', include(router.urls)),
]
