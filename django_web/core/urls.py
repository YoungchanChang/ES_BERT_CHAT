from django.urls import path
from friends import views as friend_views

app_name = "core"

urlpatterns = [path("", friend_views.HomeView.as_view(), name="home")]