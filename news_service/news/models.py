from django.contrib.auth import get_user_model
from django.db import models

MAX_LENGHT = 200
COUNT_SYMBOL_OBJ = 50

User = get_user_model()


class News(models.Model):
    title = models.CharField(
        verbose_name='Заголовок новости',
        max_length=MAX_LENGHT
    )
    text = models.TextField(verbose_name='Текст новости')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата новости'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='news',
        verbose_name='Автор'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_news'
            )
        ]

    def __str__(self):
        return f'{self.title[:COUNT_SYMBOL_OBJ]}'


class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='like',
        verbose_name='Пользователь'
    )
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='like',
        verbose_name='Новость'
    )

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'news'),
                name='unique_like'
            ),
        ]

    def __str__(self) -> str:
        return f'{self.user} лайкнул {self.news}'


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment',
        verbose_name='Автор'
    )
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='comment',
        verbose_name='Новость'
    )
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'text'),
                name='unique_comment'
            ),
        ]

    def __str__(self) -> str:
        return f'{self.author} прокомментировал {self.news}'
