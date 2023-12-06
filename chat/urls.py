# chat/urls.py
from django.urls import path
from .views import chat_home, chat_with_user, send_message, edit_message, delete_message, update_message

urlpatterns = [
    path('home/', chat_home, name='chat_home'),
    path('user/<int:user_id>/', chat_with_user, name='chat_with_user'),
    path('send_message/<int:user_id>/', send_message, name='send_message'),  # Add this line
    path('edit/<int:message_id>/', edit_message, name='edit_message'),
    path('delete/<int:message_id>/', delete_message, name='delete_message'),
    path('update/<int:message_id>/', update_message, name='update_message'),
]