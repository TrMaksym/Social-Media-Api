from rest_framework.routers import DefaultRouter

from django.urls import path, include

from blog.views import CategoryViewSet, PostViewSet, CommentViewSet, ProfileViewSet

app_name = "blog"

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)
router.register(r"profiles", ProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
]