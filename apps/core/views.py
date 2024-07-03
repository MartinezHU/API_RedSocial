from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet


class BaseViewSet(ModelViewSet):
    filter_backends = [SearchFilter, OrderingFilter]
