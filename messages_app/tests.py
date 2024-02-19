from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Message
from rest_framework.authtoken.models import Token


class MessageAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_create_message(self):
        url = reverse('message-list-create')
        data = {
            'sender': self.user.id,
            'receiver': self.user.id,
            'message': 'Test message',
            'subject': 'Test subject'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_messages(self):
        Message.objects.create(sender=self.user, receiver=self.user, message='Test message', subject='Test subject')
        url = reverse('message-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_message(self):
        message = Message.objects.create(sender=self.user, receiver=self.user, message='Test message',
                                         subject='Test subject')
        url = reverse('message-detail', kwargs={'pk': message.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Test message')

    def test_mark_message_as_read(self):
        message = Message.objects.create(sender=self.user, receiver=self.user, message='Test message',
                                         subject='Test subject')
        url = reverse('mark-message-as-read')
        data = {'message_id': message.pk}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        message.refresh_from_db()
        self.assertTrue(message.read)

    def test_last_received_message(self):
        Message.objects.create(sender=self.user, receiver=self.user, message='Test message 1', subject='Test subject')
        Message.objects.create(sender=self.user, receiver=self.user, message='Test message 2', subject='Test subject')
        url = reverse('last-received-message')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Test message 2')

    def test_unread_message_list(self):
        Message.objects.create(sender=self.user, receiver=self.user, message='Test message', subject='Test subject',
                               read=False)
        url = reverse('unread-message-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_message(self):
        # Create a message where the receiver is not the sender
        sender = User.objects.create_user(username='sender', password='sender_password')
        receiver = User.objects.create_user(username='receiver', password='receiver_password')
        message = Message.objects.create(sender=sender, receiver=receiver, message='Test message',
                                         subject='Test subject')
        # Authenticate as the receiver
        self.client.force_authenticate(user=receiver)

        # Delete the message
        url = reverse('message-detail', kwargs={'pk': message.pk})
        response = self.client.delete(url)

        # Check that the response status code is HTTP_204_NO_CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check that both sender_deleted and receiver_deleted are True
        message.refresh_from_db()
        self.assertTrue(message.receiver_deleted)

        self.client.force_authenticate(user=sender)
        response = self.client.delete(url)
        message.refresh_from_db()
        self.assertTrue(message.sender_deleted)

    def test_delete_nonexistent_message(self):
        url = reverse('message-detail', kwargs={'pk': 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_message_not_allowed(self):
        other_user = User.objects.create_user(username='other_user', password='other_password')
        message = Message.objects.create(sender=other_user, receiver=other_user, message='Test message',
                                         subject='Test subject')
        url = reverse('message-detail', kwargs={'pk': message.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
