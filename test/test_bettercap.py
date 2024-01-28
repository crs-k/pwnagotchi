import unittest
from unittest.mock import patch, Mock
from pwnagotchi import bettercap
import websockets

# AsyncMock is a helper class for mocking async functions
class AsyncMock(Mock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)

class TestClient(unittest.TestCase):
    @patch('requests.get')
    def test_session(self, mock_get):
        # Mock the response from requests.get
        mock_get.return_value.json.return_value = {'session': 'test'}

        # Initialize Client object
        client = bettercap.Client()

        # Test session function
        self.assertEqual(client.session(), {'session': 'test'})

    @patch('requests.post')
    def test_run(self, mock_post):
        # Mock the response from requests.post
        mock_post.return_value.json.return_value = {'cmd': 'test'}

        # Initialize Client object
        client = bettercap.Client()

        # Test run function
        self.assertEqual(client.run('test command'), {'cmd': 'test'})

    # Mocking async functions requires a bit more work
    @patch('websockets.connect', new_callable=AsyncMock)
    async def test_start_websocket(self, mock_connect):
        # Mock the response from websockets.connect
        mock_connect.return_value.__aenter__.return_value.recv.side_effect = ['test message', websockets.exceptions.ConnectionClosedError]

        # Initialize Client object
        client = bettercap.Client()

        # Test start_websocket function
        await client.start_websocket(Mock())

if __name__ == '__main__':
    unittest.main()