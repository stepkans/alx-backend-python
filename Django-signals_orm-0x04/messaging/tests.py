# messaging/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessageSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create(username='sender')
        self.receiver = User.objects.create(username='receiver')

    def test_notification_creation(self):
        message = Message.objects.create(
            sender=sender,
            receiver=self.receiver,
            content='Hello!'
        )
        notification = Notification.objects.filter(user=self.receiver, message=message).first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.is_read, False)
