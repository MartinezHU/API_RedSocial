from rest_framework import permissions


class IsOwnerOrStaffOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Permitir operaciones seguras (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permitir a los usuarios staff realizar operaciones de escritura
        if request.user.is_staff:
            return True

        # Permitir al propietario realizar operaciones de escritura
        return obj == request.user


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Permitir el acceso seguro (GET, HEAD, OPTIONS) para todos
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permitir a los usuarios staff realizar operaciones de escritura
        return request.user.is_staff


class IsStaffPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ['PUT', 'PATCH']:
            if request.user.is_staff or request.user.is_superuser:
                # Usuarios staff pueden editar todos los campos
                return True
            else:
                # Usuarios propietarios pueden editar todos los campos excepto "is_staff"
                return obj == request.user and 'is_staff' not in request.data
        return False

