from django.db import models
from django.contrib.auth.models import User  # Importing the User model from Django's authentication system


# Model class representing a message
class Message(models.Model):
    # Sender of the message, linked to a User object
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    # Receiver of the message, linked to a User object
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    # Content of the message
    message = models.TextField()
    # Subject of the message, limited to 50 characters
    subject = models.TextField(max_length=50)
    # Date and time when the message was created, automatically set to the current datetime when the message is created
    creation_date = models.DateTimeField(auto_now_add=True)
    # Flag indicating whether the message has been read or not, defaulting to False
    read = models.BooleanField(default=False)
