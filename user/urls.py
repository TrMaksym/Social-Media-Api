from django.urls import path

from user.views import CreateUserView, ManageUserView

app_name = "user"


urlpatterns = [
    path("registration/", CreateUserView.as_view(), name="registration"),
    path("me/", ManageUserView.as_view(), name="me"),

]