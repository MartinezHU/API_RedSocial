from rest_framework.permissions import BasePermission


class IsAuthenticatedForActions(BasePermission):
    def has_permission(self, request, view):
        # Permitir listar el contenido de los post, comentarios, etc.
        if view.action in ['list', 'retrieve']:
            return True
        # Requerir permiso para acciones cómo
        return request.user.is_authenticated
