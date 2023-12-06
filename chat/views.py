# chat/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import models  # Add this import
from .models import Message, UserStatus
from accounts.models import CustomUser
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from .models import Message, UserStatus
from accounts.models import CustomUser

@login_required
def send_message(request, user_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            sender = request.user
            recipient_user = CustomUser.objects.get(id=user_id)

            try:
                receiver_status = UserStatus.objects.get(user=recipient_user)
            except ObjectDoesNotExist:
                # If UserStatus does not exist for the recipient, create it
                receiver_status = UserStatus.objects.create(user=recipient_user)

            message = Message.objects.create(sender=sender, receiver=recipient_user, content=content)
            receiver_status.last_message = message
            receiver_status.save()

            return redirect('chat_with_user', user_id=user_id)
        else:
            return HttpResponseBadRequest("Message content cannot be empty.")
    else:
        return HttpResponseBadRequest("Invalid request method.")
    
# chat/views.py
@login_required
def chat_home(request):
    all_users = CustomUser.objects.exclude(id=request.user.id)
    user_statuses = UserStatus.objects.filter(user__in=all_users)
    
    # Create a dictionary to map user IDs to UserStatus instances
    user_status_dict = {user_status.user.id: user_status for user_status in user_statuses}
    
    # Create a list of users with their UserStatus instances (or None if not found)
    users = [
        {'user': user, 'user_status': user_status_dict.get(user.id)}
        for user in all_users
    ]

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
