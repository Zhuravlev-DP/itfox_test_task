from django.contrib.auth.models import User
from rest_framework import authentication, exceptions
from rest_framework.authtoken.models import Token


class CustomAuthentication(authentication.BaseAuthentication):
    """
    Кастомный класс авторизации.
    """
    def authenticate(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            raise exceptions.AuthenticationFailed('Введите username/password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Пользователя не существует')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Неверный пароль')
        token = Token.objects.get_or_create(user=user)
        return user, token
