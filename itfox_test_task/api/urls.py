from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

# from api.views import PostViewSet, GroupViewSet, CommentViewSet

router_v1 = DefaultRouter()
# router_v1.register(r'news', PostViewSet)
# router_v1.register(
#     r'posts/(?P<post_id>[1-9]\d*)/comments',
#     CommentViewSet,
#     basename='comments'
# )

urlpatterns = [
    path('v1/auth/', views.obtain_auth_token),
    path('v1/', include(router_v1.urls)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
