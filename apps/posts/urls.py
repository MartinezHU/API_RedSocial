from os.path import basename

from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.posts.views import PostView, RecommendedFeedView

router = SimpleRouter()

router.register(r'posts', PostView, basename='posts')
router.register(r'recommended_feed', RecommendedFeedView, basename='recommended_feed')
router.register(r'my_feed', RecommendedFeedView, basename='my_feed')

urlpatterns = [
    path('', include(router.urls))
]
