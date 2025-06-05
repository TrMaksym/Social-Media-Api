from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from user.views import CreateUserView, ManageUserView, SearchView, FollowersView, FollowingView, UnfollowView, \
    FollowView

app_name = "user"


urlpatterns = [
    path("auth/registration/", CreateUserView.as_view(), name="registration"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    path("profile/me/", ManageUserView.as_view(), name="me"),
    path("users/search/", SearchView.as_view(), name="search"),
    path("users/follow/", FollowView.as_view(), name="follow"),
    path("users/unfollow/", UnfollowView.as_view(), name="unfollow"),
    path("users/following/", FollowingView.as_view(), name="following"),
    path("users/followers/", FollowersView.as_view(), name="followers"),

]