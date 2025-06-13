from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )
        
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # Meaning the message already exists
        previous = Message.objects.get(pk=instance.pk)
        if previous.content != instance.content:
            # Store the previous content in history
            MessageHistory.objects.create(
                message=previous,
                previous_content=previous.content
            )
            # Mark message as edited
            instance.edited = True        