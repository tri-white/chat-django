# chat/urls.py
from django.urls import path
from .views import chat_home, chat_with_user

urlpatterns = [
    path('home/', chat_home, name='chat_home'),
    path('user/<int:user_id>/', chat_with_user, name='chat_with_user'),
]
