import unittest
from flask_testing import TestCase
from app import app, socketio


class FlaskAppTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_secret_key'
        return app

    def setUp(self):
        self.socketio_client = socketio.test_client(app)
        self.socketio_client.connect()

    def tearDown(self):
        self.socketio_client.disconnect()

    def test_handle_user_join(self):
        self.socketio_client.emit('user_join', 'test_user')
        received_message = self.socketio_client.get_received()
        expected_response = {'username': 'System', 'message': 'test_user joined the chat'}
        self.assertEqual(received_message[0]['args'][0], expected_response)

    def test_handle_new_message(self):
        self.socketio_client.emit('user_join', 'test_user')
        self.socketio_client.emit('new_message', 'Hello, World!')
        received_message = self.socketio_client.get_received()
        expected_response = {'username': 'test_user', 'message': 'Hello, World!'}
        self.assertEqual(received_message[1]['args'][0], expected_response)


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_login(self):
        response = self.app.post('/login', data={'username': 'test_user', 'password': 'test_password'})
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
