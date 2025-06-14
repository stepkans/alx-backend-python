from django.contrib.auth.models import User
from django.db import models
from . managers import UnreadMessagesManager


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(blank=True, null=True)
    edited_by = models.ForeignKey(User, related_name='edited_messages', on_delete=models.CASCADE, blank=True, null=True)
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self',
        related_name='replies',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    # Attach custom manager
    unread = UnreadMessagesManager()
    objects = models.Manager()

    def __str__(self):
        return f'{self.sender} -> {self.receiver}'
    
class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='notification', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} notification for message {self.message}'

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name='histories', on_delete=models.CASCADE)
    previous_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.message} (edited at {self.timestamp})'    
    