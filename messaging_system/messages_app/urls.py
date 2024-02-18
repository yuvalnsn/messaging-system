from django.urls import path
from .views import (  # Importing views from the local module
    MessageListCreateAPIView,
    UnreadMessageListAPIView,
    MessageRetrieveUpdateDestroyAPIView,
    MarkMessageAsReadAPIView
)

# URL patterns for the message-related endpoints
urlpatterns = [
    # URL pattern for listing and creating messages
    path('', MessageListCreateAPIView.as_view(), name='message-list-create'),
    # URL pattern for listing unread messages
    path('unread/', UnreadMessageListAPIView.as_view(), name='unread-message-list'),
    # URL pattern for retrieving, updating, and deleting a specific message
    path('<int:pk>/', MessageRetrieveUpdateDestroyAPIView.as_view(), name='message-detail'),
    # URL pattern for marking a message as read
    path('mark-as-read/<int:pk>/', MarkMessageAsReadAPIView.as_view(), name='mark-message-as-read')
]
