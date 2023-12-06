# chat/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import Message, UserStatus
from accounts.models import CustomUser
from django.http import HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist  # Add this import

@login_required
def send_message(request, user_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            sender = request.user
            try:
                receiver_status = UserStatus.objects.get(user__id=user_id)
                receiver = receiver_status.user
            except ObjectDoesNotExist:
                # If UserStatus does not exist, create it
                receiver = UserStatus.objects.create(user_id=user_id).user

            message = Message.objects.create(sender=sender, receiver=receiver, content=content)
            return redirect('chat_with_user', user_id=user_id)
        else:
            return HttpResponseBadRequest("Message content cannot be empty.")
    else:
        return HttpResponseBadRequest("Invalid request method.")
    
@login_required
def chat_home(request):
    users = UserStatus.objects.exclude(user=request.user)
    context = {'users': users}
    return render(request, 'chat/chat_home.html', context)

@login_required
def chat_with_user(request, user_id):
    other_user = CustomUser.objects.get(pk=user_id)
    messages = Message.objects.filter(
        (models.Q(sender=request.user) & models.Q(receiver=other_user)) |
        (models.Q(sender=other_user) & models.Q(receiver=request.user))
    ).order_by('timestamp')
    context = {'other_user': other_user, 'messages': messages}
    return render(request, 'chat/chat_with_user.html', context)
