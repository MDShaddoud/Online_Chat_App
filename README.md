# Online Chat Application Documentation


## Introduction

The Online Chat Application is a real-time messaging platform designed to facilitate communication between users. It provides features such as user registration, login, real-time chat, and message history.

## Installation

Follow these steps to set up the Online Chat Application:

1. Clone the repository:

    ```bash
    git clone https://github.com/MDShaddoud/Online_Chat_App.git
    cd Online_Chat_App
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up the database:

    ```bash
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    ```

4. Run the application:

    ```bash
    python app.py
    ```

## Usage

### Signing Up

- Access the application through the browser.
- Click on the "Sign Up" link.
- Enter a unique username and password.
- Submit the form to create an account.

### Logging In

- Access the application through the browser.
- Click on the "Log In" link.
- Enter your username and password.
- Submit the form to log in.

### Chatting

- Once logged in, you can participate in real-time chat.
- Send and receive messages in the chat window.
- Use the "Logout" link to log out.

## API Documentation

The Online Chat Application exposes a RESTful API for retrieving and posting messages. Below are the API endpoints:

- **GET /messages:** Retrieve all messages.
- **POST /messages:** Post a new message.

API requests and responses should be in JSON format.

## Unit Tests

To run unit tests, execute the following command:

```bash
python -m unittest discover -v
