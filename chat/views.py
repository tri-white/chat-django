# chat/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import models  # Add this import
from .models import Message, UserStatus, MessageCheck
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
from django.db.models import Max, F

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Message

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

            try:
                receiver_status = UserStatus.objects.get(user=recipient_user)
            except ObjectDoesNotExist:
                receiver_status = UserStatus.objects.create(user=recipient_user)

            message = Message.objects.create(sender=sender, receiver=recipient_user, content=content)

            # Update last_activity for both sender and receiver
            sender_status.last_activity = timezone.now()

            # Update the last_checked timestamp for the sender
            sender_check, created = MessageCheck.objects.get_or_create(user=sender, other_user=recipient_user)
            sender_check.last_checked = timezone.now()
            sender_check.save()

            sender_status.last_message = message

            sender_status.save()
            receiver_status.save()

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

    user_checks = MessageCheck.objects.filter(user=request.user)
    last_checked_dict = {check.other_user_id: check.last_checked for check in user_checks}

    last_messages = Message.objects.filter(receiver=request.user).values('sender').annotate(last_message=Max('timestamp'))

    last_message_dict = {message['sender']: message['last_message'] for message in last_messages}

    unchecked_users_dict = {}

    for user_status in users:
        user_id = user_status.user.id
        last_checked = last_checked_dict.get(user_id)
        last_message = last_message_dict.get(user_id)

        # Exclude the user if there are no messages
        if last_message is not None:
            # Consider the user as unread if they have never checked the messages
            if not last_checked:
                unchecked_users_dict[user_id] = last_message
            # Consider the user as unread if there are new messages since their last check
            elif last_checked and last_message > last_checked:
                unchecked_users_dict[user_id] = last_message



    context = {
        'users': users,
        'unchecked_users_dict': unchecked_users_dict,
    }
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

        # Update the last_checked timestamp when the user enters the chat
        try:
            sender_check = MessageCheck.objects.get(user=request.user, other_user=other_user)
        except MessageCheck.DoesNotExist:
            sender_check = MessageCheck.objects.create(user=request.user, other_user=other_user)

        sender_check.last_checked = timezone.now()
        sender_check.save()

    except ObjectDoesNotExist:
        last_activity = None

    context = {
        'other_user': other_user,
        'messages': messages,
        'last_activity': last_activity,
        'current_user': request.user,  # Pass the current user to the template
    }    
    
    return render(request, 'chat/chat_with_user.html', context)

@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user)

    if message.content == "deleted message":
        return HttpResponseForbidden("You cannot edit a deleted message.")

    context = {'message': message}
    return render(request, 'chat/edit_message.html', context)

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    # Update message content to "deleted message"
    message.content = "deleted message"
    message.save()
    return redirect('chat_with_user', user_id=message.receiver.id)

@login_required
def update_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user)

    if message.content == "deleted message":
        # Do not allow further updates for "deleted message"
        return HttpResponseForbidden("You cannot edit a deleted message.")

    if request.method == 'POST':
        new_content = request.POST.get('content')
        message.content = new_content
        message.save()

    return redirect('chat_with_user', user_id=message.receiver.id)