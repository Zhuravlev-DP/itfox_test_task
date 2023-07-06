from django.shortcuts import get_object_or_404
from rest_framework import authentication, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsAuthorOrAdmin, IsAuthorNews
from api.serializers import CommentSerializer, LikeSerializer, NewsSerializer
from news.models import Like, News


class CreateListRetrieveDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Собственный базовый класс вьюсета."""
    pass


class NewsViewSet(viewsets.ModelViewSet):
    """Вьюсет обработки новостей."""
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrAdmin)
    authentication_classes = [authentication.TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['POST', 'DELETE'], detail=True)
    def like(self, request, pk):
        """Добавляет/удалет лайк новости."""
        user = self.request.user
        news = get_object_or_404(News, pk=pk)
        object = Like.objects.filter(
            user=user,
            news=news
        )

        if self.request.method == 'POST':
            serializer = LikeSerializer(
                data={'user': user.id, 'news': pk},
                context={'request': self.request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if object.exists():
            object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'У этой новости не было лайка'},
            status=status.HTTP_400_BAD_REQUEST
        )


class CommentViewSet(CreateListRetrieveDestroyViewSet):
    """Вьюсет обработки комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrAdmin)
    authentication_classes = [authentication.TokenAuthentication]

    def get_news(self):
        """Получить новость из переданного news_id."""
        return get_object_or_404(News, id=self.kwargs.get('news_id'))

    def get_queryset(self):
        """Кверисет комментариев полученной новости."""
        return self.get_news().comment.all()

    def perform_create(self, serializer):
        """Передать объект пользователя, полученную новость."""
        serializer.save(
            author=self.request.user,
            news=self.get_news()
        )

    def get_permissions(self):
        """При DELETE-запросе вернуть пермишен IsAuthorNews."""
        if self.action == 'destroy':
            return (IsAuthorNews(),)
        return super().get_permissions()
