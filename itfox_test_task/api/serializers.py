from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from news.models import Comment, Like, News


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор обработки комментариев."""
    author = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    news = serializers.SlugRelatedField(
        slug_field='title',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('news',)
        validators = [
            UniqueTogetherValidator(
                queryset=Comment.objects.all(),
                fields=('author', 'text')
            )
        ]


class NewsSerializer(serializers.ModelSerializer):
    """Сериализатор обработки новостей."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    comments = serializers.SerializerMethodField('get_less_comments')
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = (
            'id',
            'author',
            'pub_date',
            'title',
            'text',
            'comments_count',
            'likes_count',
            'comments',
        )

    def get_less_comments(self, obj):
        """Получить 10 комментариев и вернуть ответ через CommentSerializer."""
        comments = Comment.objects.filter(news=obj)[:10]
        serializer = CommentSerializer(instance=comments, many=True)
        return serializer.data

    def get_comments_count(self, obj):
        """Подсчет количества комментариев."""
        return obj.comment.count()

    def get_likes_count(self, obj):
        """Подсчет количества лайков."""
        return obj.like.count()


class LikeSerializer(serializers.ModelSerializer):
    """Сериализатор добавления/удаления лайков к новостям."""
    class Meta:
        model = Like
        fields = ('user', 'news')

    def validate(self, data):
        """Валидация при добавлении лайка новости."""
        user, news = data['user'], data['news']
        if Like.objects.filter(user=user, news=news).exists():
            raise serializers.ValidationError(
                {'error': 'Вы уже поставили лайк этой новости'}
            )
        return data

    def to_representation(self, instance):
        """Возвращает ответ через NewsSerializer."""
        context = {'request': self.context.get('request')}
        serializer = NewsSerializer(
            instance=instance.news,
            context=context
        )
        return serializer.data
