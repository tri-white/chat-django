# chat/models.py
from django.db import models
from accounts.models import CustomUser
from django.utils import timezone

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} to {self.receiver.username} - {self.timestamp}'



class UserStatus(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    last_message = models.ForeignKey('Message', on_delete=models.SET_NULL, null=True, blank=True)
    last_activity = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - Online: {self.is_online}'
    
class MessageCheck(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='message_checks')
    other_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='checked_messages_from')
    last_checked = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'other_user')