from django.http import HttpResponse
from rest_framework import status
from apps.core.views import BaseViewSet


class EnsureAuthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Obtener la vista actual desde resolver_match
        view = getattr(request, 'resolver_match', None)

        # Verificar si la vista actual es una instancia de BaseViewSet
        if view and hasattr(view.func, 'cls') and issubclass(view.func.cls, BaseViewSet):
            if not request.user.is_authenticated:
                return HttpResponse('Unauthorized: Authentication Required', status=status.HTTP_401_UNAUTHORIZED)

        return response
