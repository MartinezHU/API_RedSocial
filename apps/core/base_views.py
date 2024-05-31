from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.core.responses import CustomPagination
from apps.core.serializers import CustomPaginationSerializer


class BaseViewSet(ModelViewSet):
    pagination_class = CustomPagination

    @extend_schema(
        summary="List resources",
        responses={
            200: OpenApiResponse(response=CustomPaginationSerializer(many=True),
                                 description='List of resources'),
            400: OpenApiResponse(description='Bad request (something invalid)'),
        },
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
