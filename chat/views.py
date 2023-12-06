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
from django.utils import timezone
from django.db.models import Q

@login_required
def send_message(request, user_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            sender = request.user
            recipient_user = CustomUser.objects.get(id=user_id)

            try:
                sender_status = UserStatus.objects.get(user=sender)
            except ObjectDoesNotExist:
                sender_status = UserStatus.objects.create(user=sender)

            message = Message.objects.create(sender=sender, receiver=recipient_user, content=content)

            sender_status.last_activity = timezone.now()

            sender_status.last_message = message

            sender_status.save()

            return redirect('chat_with_user', user_id=user_id)
        else:
            return HttpResponseBadRequest("Message content cannot be empty.")
    else:
        return HttpResponseBadRequest("Invalid request method.")
    
@login_required
def chat_home(request):
    if request.method == 'GET' and 'search' in request.GET:
        search_query = request.GET.get('search')
        users = UserStatus.objects.filter(
            Q(user__username__icontains=search_query)
        ).exclude(user=request.user)
    else:
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

    try:
        other_user_status = UserStatus.objects.get(user=other_user)
        last_activity = other_user_status.last_activity
    except ObjectDoesNotExist:
        last_activity = None

    context = {'other_user': other_user, 'messages': messages, 'last_activity': last_activity}
    return render(request, 'chat/chat_with_user.html', context)