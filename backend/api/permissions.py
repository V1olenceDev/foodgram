from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Право доступа, которое разрешает неавторизованным пользователям
    только безопасные методы запросов.
    Авторизованным пользователям разрешает
    редактирование объектов, если они являются авторами этих объектов.
    """
    def has_permission(self, request, view):
        """
        Проверка общего разрешения для запроса.
        Разрешает безопасные методы (такие как GET) для всех пользователей и
        все методы для аутентифицированных пользователей.
        """
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """
        Проверка разрешения для конкретного объекта.
        Разрешает доступ только если метод безопасен
        или если пользователь является автором объекта.
        """
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
