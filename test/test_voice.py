import unittest
from unittest.mock import MagicMock, patch
from pwnagotchi.voice import Voice

class TestVoice(unittest.TestCase):
    def setUp(self):
        self.gettext_mock = MagicMock()
        self.voice = Voice('en')
        self.voice._ = self.gettext_mock

    def test_default(self):
        self.voice.default()
        self.gettext_mock.assert_called_with('Sleeping.')

    def test_on_starting(self):
        self.voice.on_starting()
        self.gettext_mock.assert_called_with('Pwnagotchi! Starting...')

    def test_on_ai_ready(self):
        self.voice.on_ai_ready()
        self.gettext_mock.assert_called_with('AI ready.')

    def test_on_keys_generation(self):
        self.voice.on_keys_generation()
        self.gettext_mock.assert_called_with('Generating keys, do not turn off.')

    def test_on_normal(self):
        self.voice.on_normal()
        self.gettext_mock.assert_called_with('Feeling normal.')

    @patch('gettext.translation')
    def test_on_free_channel(self, mock_translation):
        mock_gettext = mock_translation.return_value.gettext
        mock_gettext.return_value = 'Hey, channel {channel} is free! Your AP will say thanks.'
        
        voice = Voice('en')
        channel = 1
        result = voice.on_free_channel(channel)
        
        mock_gettext.assert_called_once_with('Hey, channel {channel} is free! Your AP will say thanks.')
        self.assertEqual(result, 'Hey, channel 1 is free! Your AP will say thanks.')


    def test_on_reading_logs(self):
        self.voice.on_reading_logs(0)
        self.gettext_mock.assert_called_with('Reading last session logs.')
        self.voice.on_reading_logs(100)
        self.gettext_mock.assert_called_with('Read {lines_so_far} log lines so far.')

    # Continue with the rest of the methods in a similar fashion...

if __name__ == '__main__':
    unittest.main()