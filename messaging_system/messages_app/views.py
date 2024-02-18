from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Message  # Importing the Message model from the local module
from .serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


# API endpoints for listing and creating messages
class MessageListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    # Handler for GET requests to retrieve messages
    def get(self, request):
        messages = Message.objects.filter(
            Q(receiver=request.user) | Q(
                sender=request.user))  # Fetch messages for the logged-in user. Q() allows you to perform logical OR operations between these conditions.
        serializer = MessageSerializer(messages, many=True)  # Serialize fetched messages
        return Response(serializer.data)  # Return serialized data as a response

    # Handler for POST requests to create a new message
    def post(self, request):
        request.data['sender'] = request.user.id  # Assuming sender is the user id
        serializer = MessageSerializer(data=request.data)  # Deserialize incoming message data
        if serializer.is_valid():  # Check if deserialized data is valid
            serializer.save(sender=request.user)  # Save the message with the logged-in user as the sender
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)  # Return serialized data with 201 Created status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return errors if data is not valid


# API endpoints for listing unread messages
class UnreadMessageListAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    # Handler for GET requests to retrieve unread messages
    def get(self, request):
        unread_messages = Message.objects.filter(receiver=request.user,
                                                 read=False)  # Fetch unread messages for the logged-in user
        serializer = MessageSerializer(unread_messages, many=True)  # Serialize fetched messages
        return Response(serializer.data)  # Return serialized data as a response


# API endpoints for retrieving, updating, and deleting a specific message
class MessageRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    # Helper function to retrieve a message by its primary key
    def get_object(self, pk):
        try:
            return Message.objects.get(pk=pk)  # Retrieve message by primary key
        except Message.DoesNotExist:  # Handle case where message does not exist
            raise status.HTTP_404_NOT_FOUND  # Raise 404 Not Found error

    # Handler for GET requests to retrieve a specific message
    def get(self, request, pk):
        message = self.get_object(pk)  # Retrieve the message
        serializer = MessageSerializer(message)  # Serialize the message
        return Response(serializer.data)  # Return serialized data as a response

    # Handler for DELETE requests to delete a specific message
    def delete(self, request, pk):
        message = self.get_object(pk)  # Retrieve the message
        message.delete()  # Delete the message
        return Response(status=status.HTTP_204_NO_CONTENT)  # Return 204 No Content status


# API endpoint for marking a message as read
class MarkMessageAsReadAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    # Handler for PATCH requests to mark a message as read
    def patch(self, request, pk):
        try:
            message = Message.objects.get(pk=pk, receiver=request.user)  # Retrieve the message for the logged-in user
            message.mark_as_read()   # Mark the message as read
            serializer = MessageSerializer(message)  # Serialize the updated message
            return Response(serializer.data)  # Return serialized data as a response
        except Message.DoesNotExist:  # Handle case where message does not exist
            return Response(status=status.HTTP_404_NOT_FOUND)  # Return 404 Not Found error
