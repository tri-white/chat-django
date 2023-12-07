# mychat/urls.py
from django.contrib import admin
from django.urls import path, include
from .views import index 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('chat/', include('chat.urls')),
    path('', index, name='index'),
]