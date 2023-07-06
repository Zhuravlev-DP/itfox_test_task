from django.contrib import admin

from news.models import Comment, Like, News


class CommentsInstanceInline(admin.TabularInline):
    model = Comment


class LikesInstanceInline(admin.TabularInline):
    model = Like


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'text', 'title')

    inlines = [CommentsInstanceInline, LikesInstanceInline]
