from rest_framework.views import APIView  # Importing APIView from rest_framework.views
from rest_framework.response import Response  # Importing Response from rest_framework.response
from rest_framework import status  # Importing status from rest_framework
from .models import Message  # Importing the Message model from the local module
from .serializers import MessageSerializer  # Importing the MessageSerializer from the local module
from rest_framework.permissions import IsAuthenticated  # Importing IsAuthenticated from rest_framework.permissions
from django.db.models import Q  # Importing Q from django.db.models to perform complex queries
from django.shortcuts import \
    get_object_or_404  # Importing get_object_or_404 from django.shortcuts to get an object or return 404
from django.http import Http404  # Importing Http404 from django.http to raise a 404 error
import logging  # Importing logging module for logging purposes

logger = logging.getLogger(__name__)  # Creating a logger object with the current module name


# API endpoints for listing and creating messages
class MessageListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]  # can be used only for authenticated users

    # Handler for GET requests to retrieve a list of messages
    def get(self, request):
        try:
            # Filtering messages where the logged in user is either the reciever or the sender, and the message is not deleted
            messages = Message.objects.filter(
                Q(receiver=request.user, receiver_deleted=False) | Q(sender=request.user, sender_deleted=False)
            )
            serializer = MessageSerializer(messages, many=True)  # Serializing the messages
            return Response(serializer.data, status=status.HTTP_200_OK)  # Returning serialized data with success status
        except Exception as e:
            logger.error(f"Failed to fetch messages: {str(e)}")
            return Response(
                {"error": "Failed to fetch messages."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )  # Returning error response with 500 status code in case of failure

    # Handler for POST requests to create a new message
    def post(self, request):
        try:
            request.data["sender"] = request.user.id  # Assigning sender ID from current user
            serializer = MessageSerializer(data=request.data)  # Creating serializer instance with request data
            if serializer.is_valid():  # Checking if serializer data is valid
                serializer.save(sender=request.user)  # Saving the message with the sender as the current user
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)  # Returning serialized data with success status
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )  # Returning error response with 400 status code for invalid data
        except Exception as e:
            logger.error(f"Failed to create message: {str(e)}")
            return Response(
                {"error": "Failed to create message."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# API endpoints for listing unread messages
class UnreadMessageListAPIView(APIView):
    permission_classes = [IsAuthenticated]  # can be used only for authenticated users

    # Handler for GET requests to retrieve unread messages
    def get(self, request):
        try:
            # Filtering unread messages for the current user
            unread_messages = Message.objects.filter(receiver=request.user, read=False, receiver_deleted=False)
            serializer = MessageSerializer(unread_messages, many=True)  # Serializing the unread messages
            return Response(serializer.data, status=status.HTTP_200_OK)  # Returning serialized data with success status
        except Exception as e:
            logger.error(f"Failed to fetch unread messages: {str(e)}")
            return Response(
                {"error": "Failed to fetch unread messages."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )  # Returning error response with 500 status code in case of failure


# API endpoint for retrieving the last received message
class LastReceivedMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]  # can be used only for authenticated users

    # Handler for GET requests to retrieve the last received message
    def get(self, request):
        try:
            # Retrieving the last received message for the current user
            last_message = Message.objects.filter(receiver=request.user, receiver_deleted=False).latest('creation_date')
            serializer = MessageSerializer(last_message)  # Serializing the last received message
            return Response(serializer.data, status=status.HTTP_200_OK)  # Returning serialized data with success status
        except Message.DoesNotExist:  # Handling case where message does not exist
            return Response(status=status.HTTP_404_NOT_FOUND)  # Returning 404 Not Found error
        except Exception as e:
            logger.error(f"Failed to fetch last message: {str(e)}")
            return Response(
                {"error": "Failed to fetch last message."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )  # Returning error response with 500 status code in case of failure


# API endpoint for retrieving, updating, and deleting a message
class MessageRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated]  # can be used only for authenticated users

    # Method to get the message object with given primary key
    def get_object(self, pk):
        try:
            # Getting the message object or raising 404 if not found
            message = get_object_or_404(Message, pk=pk)
            if message.is_deleted_for_user(self.request.user):
                raise Http404("Message does not exist or has been deleted.")
            return message
        except Http404 as e:
            raise e  # Re-raising Http404 exceptions to return appropriate HTTP status

    # Handler for GET requests to retrieve a message
    def get(self, request, pk):
        try:
            message = self.get_object(pk)  # Getting the message object
            serializer = MessageSerializer(message)  # Serializing the message
            return Response(serializer.data, status=status.HTTP_200_OK)  # Returning serialized data with success status
        except Http404 as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )  # Returning 404 Not Found error if message not found
        except Exception as e:
            logger.error(f"Failed to retrieve message: {str(e)}")
            return Response(
                {"error": "Failed to retrieve message."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )  # Returning error response with 500 status code in case of failure

    # Handler for DELETE requests to delete a message
    def delete(self, request, pk):
        try:
            message = self.get_object(pk)  # Getting the message object
            message.delete_for_user(request.user)  # Deleting the message for the user
            return Response(status=status.HTTP_204_NO_CONTENT)  # Returning success response with no content
        except Http404 as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )  # Returning 404 Not Found error if message not found
        except Exception as e:
            logger.error(f"Failed to delete message: {str(e)}")  # Logging error message
            return Response(
                {"error": "Failed to delete message."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )  # Returning error response with 500 status code in case of failure


# API endpoint for marking a message as read
class MarkMessageAsReadAPIView(APIView):
    permission_classes = [IsAuthenticated]  # can be used only for authenticated users

    # Handler for PATCH requests to mark a message as read
    def patch(self, request):
        try:
            message_id = request.data.get('message_id')  # Getting the message ID from request data
            # Retrieving the message for the logged-in user
            message = Message.objects.get(pk=message_id, receiver=request.user, receiver_deleted=False)
            message.mark_as_read()  # Marking the message as read
            return Response(status=status.HTTP_204_NO_CONTENT)  # Returning success response with no content
        except Message.DoesNotExist:  # Handling case where message does not exist
            return Response(status=status.HTTP_404_NOT_FOUND)  # Returning 404 Not Found error
        except Exception as e:
            logger.error(f"Failed to mark message as read: {str(e)}")  # Logging error message
            return Response(
                {"error": "Failed to mark message as read."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )  # Returning error response with 500 status code in case of failure
