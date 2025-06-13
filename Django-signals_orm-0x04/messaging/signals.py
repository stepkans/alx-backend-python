from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save,post_delete
from django.contrib.auth.models import User
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

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # This might be redundant if CASCADE is already enforced
    # but it's a helpful fallback or for additional cleanup.
    from .models import Message, Notification, MessageHistory

    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()            