from rest_framework.routers import DefaultRouter

from django.urls import path, include

from blog.views import CategoryViewSet, PostViewSet, CommentViewSet, ProfileViewSet, CommentModerationViewSet, \
    FollowViewSet, PostMediaViewSet

app_name = "blog"

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)
router.register(r"comment-moderation", CommentModerationViewSet, basename="comment-moderation")
router.register(r"profiles", ProfileViewSet)
router.register(r"follows", FollowViewSet, basename="follows")

urlpatterns = [
    path("", include(router.urls)),
path(
        "posts/<int:post_pk>/media/",
        PostMediaViewSet.as_view({"get": "list", "post": "create"}),
        name="post-media-list",
    ),
    path(
        "posts/<int:post_pk>/media/<int:pk>/",
        PostMediaViewSet.as_view({"get": "retrieve", "delete": "destroy"}),
        name="post-media-detail",
    ),
]
