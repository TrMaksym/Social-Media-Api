from django.urls import path

import user

app_name = user


urlpatterns = [
    path("registration/", CreateUserView.as_view(), name="registration"),
    path("me/", ManageUserView.as_view(), name="me"),

]