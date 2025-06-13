from django.db import models
class UnreadMessagesManager(models.Manager):
    """Custom manager for retrieving unread messages for a user."""
    def for_user(self, user):
        return self.filter(receiver=user, read=False).only('id', 'sender_id', 'receiver_id', 'read', 'content')