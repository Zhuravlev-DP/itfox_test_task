from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from api.views import CommentViewSet, NewsViewSet

router_v1 = DefaultRouter()
router_v1.register(r'news', NewsViewSet)
router_v1.register(
    r'news/(?P<news_id>[1-9]\d*)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', views.obtain_auth_token),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
