from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Category, Post, Comment, Profile, Follow, PostMedia
from blog.serializers import (
    CategorySerializer,
    PostSerializer,
    CommentSerializer,
    ProfileSerializer,
    FollowSerializer,
    PostMediaSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PostViewSet(viewsets.ModelViewSet):
    queryset = (
        Post.objects.all()
        .select_related("author")
        .prefetch_related("categories", "likes")
    )
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["categories__slug", "tags__slug"]
    search_fields = ["title", "content"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated:
            return queryset.filter(is_published=True) | queryset.filter(author=user)
        return queryset.filter(is_published=True)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if user in post.likes.all():
            return Response(
                {"detail": "Already liked."}, status=status.HTTP_400_BAD_REQUEST
            )
        post.likes.add(user)
        return Response({"detail": "Post liked."})

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if user not in post.likes.all():
            return Response(
                {"detail": "You have not liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        post.likes.remove(user)
        return Response({"detail": "Post unliked."})


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related("post", "user")
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_approved=True)


class CommentModerationViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        comment = self.get_object()
        comment.is_approved = True
        comment.save()
        return Response({"status": "comment approved"})

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        comment = self.get_object()
        comment.is_approved = False
        comment.save()
        return Response({"status": "comment rejected"})


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().select_related("user")
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ["user__username", "bio"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

    @action(detail=False, methods=["get"])
    def followers(self, request):
        user = request.user
        followers = Follow.objects.filter(following=user)
        serializer = self.get_serializer(followers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def following(self, request):
        user = request.user
        following = Follow.objects.filter(follower=user)
        serializer = self.get_serializer(following, many=True)
        return Response(serializer.data)


class PostMediaViewSet(viewsets.ModelViewSet):
    serializer_class = PostMediaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return PostMedia.objects.filter(post_id=self.kwargs["post_pk"])

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["post_pk"])
        serializer.save(post=post)
