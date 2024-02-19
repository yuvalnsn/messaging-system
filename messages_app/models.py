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
    sender_deleted = models.BooleanField(default=False)
    receiver_deleted = models.BooleanField(default=False)

    def mark_as_read(self):
        self.read = True  # Mark the message as read
        self.save()  # Save the updated message

    def delete_for_sender(self):
        self.sender_deleted = True
        self.save()

    def delete_for_receiver(self):
        self.receiver_deleted = True
        self.save()

    def is_deleted_for_user(self, user):
        if user == self.sender:
            return self.sender_deleted
        elif user == self.receiver:
            return self.receiver_deleted
        else:
            return False

# need to comment
    def delete_for_user(self, user):
        if user == self.sender:
            self.delete_for_sender()
        if user == self.receiver:
            self.delete_for_receiver()
