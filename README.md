# Messaging System

A simple REST API backend system for handling messages between users.

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)
- [Contact Information](#contact-information)
- [Examples and Screenshots](#examples-and-screenshots)
- [FAQs](#faqs)

## Description

The Messaging System is a REST API backend built to facilitate communication between users. It allows users to send, receive, read, and delete messages, as well as retrieve all messages or unread messages for a specific user.

## Installation

1. Clone the repository: `git clone https://github.com/yuvalnsn/messaging-system.git`
2. Install virtualenv if you haven't already: `pip install virtualenv`
3. Create a virtual environment: `virtualenv myenv`
4. Activate the virtual environment 
  on windows: `myenv\Scripts\activate`
On Unix or MacOS:`source myenv/bin/activate`
5. Navigate into project directory: `cd messaging_system`
6. Install the requirements: `python -m pip install -r requirements.txt`
7. migrations?
8. Run server: `python manage.py runserver`

## Usage

To use the Messaging System, follow the API documentation provided below.

## API Documentation

- **Write Message**: POST `/api/messages`
  - Example request:
    ```json
    {
      "sender": "user1",
      "receiver": "user2",
      "message": "Hello, how are you?",
      "subject": "Greetings"
    }
    ```
- **Get All Messages for a Specific User**: GET `/api/messages/:userId`
- **Get All Unread Messages for a Specific User**: GET `/api/messages/:userId/unread`
- **Read Message**: GET `/api/messages/:messageId`
- **Delete Message**: DELETE `/api/messages/:messageId`

## Testing

To run tests, use the following command:

```bash
npm test
