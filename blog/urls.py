from .views import HomeView
from django.urls import path


app_name = "blog"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
