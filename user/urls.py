from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from user.views import CreateUserView, ManageUserView, SearchView, FollowersView, FollowingView, UnfollowView, \
    FollowView

app_name = "user"


urlpatterns = [
    path("auth/registration/", CreateUserView.as_view(), name="registration"),
    path("me/", ManageUserView.as_view(), name="me"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("search/", SearchView.as_view(), name="search"),
    path("follow/", FollowView.as_view(), name="follow"),
    path("unfollow/", UnfollowView.as_view(), name="unfollow"),
    path("following/", FollowingView.as_view(), name="following"),
    path("followers/", FollowersView.as_view(), name="followers"),

]