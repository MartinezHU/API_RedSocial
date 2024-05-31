from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.users.views import UsuarioView

router = SimpleRouter()

router.register(r'usuario', UsuarioView, basename="usuario")


urlpatterns = [
    path('', include(router.urls)),
]
