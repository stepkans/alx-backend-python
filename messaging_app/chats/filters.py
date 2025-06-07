import django_filters
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.ModelChoiceFilter(field_name="sender", queryset=User.objects.all())
    recipient = django_filters.ModelChoiceFilter(field_name="conversation__participants", queryset=User.objects.all())
    created_at__gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'created_at__gte', 'created_at__lte']
