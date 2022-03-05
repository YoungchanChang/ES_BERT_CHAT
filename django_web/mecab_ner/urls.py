from django.urls import path
from . import views
from .views import index

app_name = "mecab_ner"

urlpatterns = [path("", index, name="list"),]