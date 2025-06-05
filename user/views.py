from django.shortcuts import render
from rest_framework import generics, filters
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from user.serializers import UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class SearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username", "email")


class FollowView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=400)

        to_follow = get_object_or_404(User, email=email)

        if to_follow == request.user:
            return Response({"error": "Cannot follow yourself"}, status=400)

        request.user.following.add(to_follow)
        return Response({"detail": f"Now following {email}"}, status=200)


class UnfollowView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=400)

        to_unfollow = get_object_or_404(User, email=email)

        request.user.following.remove(to_unfollow)
        return Response({"detail": f"Unfollowed {email}"}, status=200)


class FollowingView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.following.all()


class FollowersView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.followers.all()