# Messaging System

A simple REST API backend system for handling messages between users.

## Table of Contents

- [IMPORTANT POINTS REGARDING ASSIGMENT](#IMPORTANT POINTS REGARDING ASSIGMENT)
- [Description](#description)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Examples and Screenshots](#examples-and-screenshots)

## **IMPORTANT** POINTS REGARDING ASSIGMENT
1. Regarding the 'Read/Fetch message' requirement: I decided to split the logic into 2 endpoints. Instead of marking the message as 'read' as soon as it is sent back to the client, I opted to expose another endpoint for PATCH requests that acknowledge to the server that the requested message did indeed reach the client. This decision was made because I assumed that a response from the server could fail.


2. I used Token authentication. For convenience, within the Postman file, I created a Token variable to store the received token after login. Additionally, I've added 'Pre-request scripts' for each request to extract the token and inject it into the headers for authorization. This is solely for the convenience of checking the assignment. Feel free to remove the scripts (though you will need to enter the token manually in order to use the endpoints).


3. If anything is unclear, I will be more than happy to clarify.
## Description

The Messaging System is a REST API backend built to facilitate communication between users. It allows users to send,
receive, read, and delete messages, as well as retrieve all messages or unread messages for a specific user.


## Installation

1. Clone the repository: `git clone https://github.com/yuvalnsn/messaging-system.git`
2. Install virtualenv if you haven't already: `pip install virtualenv`
3. Create a virtual environment: `virtualenv myenv`
4. Activate the virtual environment on windows: `myenv\Scripts\activate`
   On Unix or MacOS:`source myenv/bin/activate`
5. Install the requirements: `python -m pip install -r requirements.txt`
6. migrations?
7. Run server: `python manage.py runserver`

## API Documentation

- **Login**: POST `/auth/login/`
    - Example request:
      ```json
      {
        "username": "username",
        "password": "password"
      }
      ```
- **Send message**: POST `/messages/`
    - Example request:
      ```json
      {
        "receiver": 3, #int
        "subject": "Just saying hello2",
        "message": "Hello from Yuval2"
      }
      ```
- **Mark message as read**: PATCH `/messages/`
    - Example request:
      ```json
      {
        "message_id": 14 #int
      }
      ```
- **Get All Messages for a Specific User**: GET `/messages/`
- **Get All Unread Messages for a Specific User**: GET `/messages/unread/:userId<int>/`
- **Retrieve Specific Message**: GET `/messages/:messageId<int>/`
- **Retrieve Last Received Message**: GET `/messages/last-received-message/`
- **Delete message**: DELETE `/messages/:<messageId>/` 

## Testing

To run tests, use the following command (make sure you're on the main path):

```bash
python manage.py test messages_app
