from rest_framework import serializers  # Importing serializers module from rest_framework
from .models import Message  # Importing the Message model from the local module


# Serializer class for the Message model
class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message  # Define the model to be serialized
        fields = ['id', 'sender', 'receiver', 'message', 'subject', 'creation_date',
                  'read']  # Define fields to be included in the serialization

