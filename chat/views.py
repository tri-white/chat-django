# chat/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message, UserStatus

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
