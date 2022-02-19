# chat/urls.py
from django.urls import path

from chats import views as chat_views

app_name = "chat"

urlpatterns = [
    path('', chat_views.index, name='index'),
    path('<str:room_name>/', chat_views.room, name='room')
]