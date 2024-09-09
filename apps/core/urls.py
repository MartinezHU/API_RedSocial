"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework import routers

from apps.authentication.urls import router as auth_router
from apps.users.urls import router as users_router
from apps.posts.urls import router as posts_router

router = routers.DefaultRouter()
router.registry.extend(auth_router.registry)
router.registry.extend(users_router.registry)
router.registry.extend(posts_router.registry)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  # path('api/v1', include(router.urls)),
                  path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                  path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
                  path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
                  path('api-auth/', include('rest_framework.urls')),
                  path('api/auth/', include('apps.authentication.urls')),
                  path('api/users/', include('apps.users.urls')),
                  path('api/posts/', include('apps.posts.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
