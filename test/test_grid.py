import unittest
from unittest.mock import patch, Mock
from pwnagotchi import grid

class TestGrid(unittest.TestCase):
    @patch('requests.get')
    def test_is_connected(self, mock_get):
        # Mock the response from requests.get
        mock_get.return_value.json.return_value = {'isUp': True}

        # Test is_connected function
        self.assertTrue(grid.is_connected())

        # Change the mock to return False
        mock_get.return_value.json.return_value = {'isUp': False}

        # Test is_connected function again
        self.assertFalse(grid.is_connected())

    @patch('requests.get')
    @patch('requests.post')
    def test_call(self, mock_post, mock_get):
        # Mock the response from requests.get and requests.post
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'data': 'test'}
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'data': 'test'}

        # Test call function with GET request
        self.assertEqual(grid.call('/test'), {'data': 'test'})

        # Test call function with POST request and dict data
        self.assertEqual(grid.call('/test', {'key': 'value'}), {'data': 'test'})

        # Test call function with POST request and non-dict data
        self.assertEqual(grid.call('/test', 'test data'), {'data': 'test'})

        # Change the mock to return status code 400
        mock_get.return_value.status_code = 400
        mock_get.return_value.text = 'Error'
        mock_post.return_value.status_code = 400
        mock_post.return_value.text = 'Error'

        # Test call function with GET request and expect an exception
        with self.assertRaises(Exception):
            grid.call('/test')

        # Test call function with POST request and dict data and expect an exception
        with self.assertRaises(Exception):
            grid.call('/test', {'key': 'value'})

        # Test call function with POST request and non-dict data and expect an exception
        with self.assertRaises(Exception):
            grid.call('/test', 'test data')

if __name__ == '__main__':
    unittest.main()