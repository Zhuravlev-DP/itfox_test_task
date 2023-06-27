from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrAdmin(BasePermission):
    """
    Разрешение на изменение только для автора и админа.
    Остальным только чтение.
    """
    message = 'Вы должны быть автором'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_staff
        )


class IsAuthorNews(BasePermission):
    """
    Разрешение на изменение только для автора новости/комментария и админа.
    """
    message = 'Вы должны быть автором новости'

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or obj.news.author == request.user
            or request.user.is_staff
        )
