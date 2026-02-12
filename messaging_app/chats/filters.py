import django_filters
from .models import Message, Conversation
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    # Filter by sender
    sender = django_filters.ModelChoiceFilter(
        field_name='sender', queryset=User.objects.all()
    )

    # Filter by conversation participants
    participant = django_filters.ModelChoiceFilter(
        field_name='conversation__participants', queryset=User.objects.all()
    )

    # Filter by sent_at range
    start_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'participant', 'start_date', 'end_date']
