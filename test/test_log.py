import unittest
import logging
import warnings
from unittest import mock
from pwnagotchi.log import setup_logging
from pwnagotchi.log import LastSession, parse_max_size
from pwnagotchi.voice import Voice
from pwnagotchi.mesh.peer import Peer


class TestLastSession(unittest.TestCase):
    def setUp(self):
        self.config = {
            'main': {
                'lang': 'en',
                'log': {
                    'path': '/path/to/log'
                }
            }
        }
        self.last_session = LastSession(self.config)

    def test_init(self):
        self.assertEqual(self.last_session.config, self.config)
        self.assertEqual(self.last_session.path, '/path/to/log')
        self.assertEqual(self.last_session.last_session, [])
        self.assertEqual(self.last_session.last_session_id, '')
        self.assertEqual(self.last_session.last_saved_session_id, '')
        self.assertEqual(self.last_session.duration, '')
        self.assertEqual(self.last_session.duration_human, '')
        self.assertEqual(self.last_session.deauthed, 0)
        self.assertEqual(self.last_session.associated, 0)
        self.assertEqual(self.last_session.handshakes, 0)
        self.assertEqual(self.last_session.peers, 0)
        self.assertEqual(self.last_session.last_peer, None)
        self.assertEqual(self.last_session.epochs, 0)
        self.assertEqual(self.last_session.train_epochs, 0)
        self.assertEqual(self.last_session.min_reward, 1000)
        self.assertEqual(self.last_session.max_reward, -1000)
        self.assertEqual(self.last_session.avg_reward, 0)
        self.assertEqual(self.last_session.parsed, False)

    def test_is_new(self):
        self.last_session.last_session_id = '123'
        self.last_session.last_saved_session_id = '456'
        self.assertTrue(self.last_session.is_new())

        self.last_session.last_saved_session_id = '123'
        self.assertFalse(self.last_session.is_new())

class TestParseMaxSize(unittest.TestCase):
    def test_parse_max_size(self):
        self.assertEqual(parse_max_size('10k'), 10240)
        self.assertEqual(parse_max_size('10m'), 10485760)
        self.assertEqual(parse_max_size('10g'), 10737418240)
        self.assertEqual(parse_max_size('10'), 10)
        self.assertEqual(parse_max_size('10x'), 10)  # Expecting the function to return the number part

class TestSetupLogging(unittest.TestCase):
    @mock.patch('pwnagotchi.log.logging')
    @mock.patch('pwnagotchi.log.warnings')
    def test_setup_logging(self, mock_warnings, mock_logging):
        args = mock.Mock()
        args.debug = False
        config = {
            'main': {
                'log': {
                    'path': '/path/to/log',
                    'rotation': {
                        'enabled': True,  # or False, depending on your test case
                        # include other keys that log_rotation function might use
                }
                }
            }
        }

        setup_logging(args, config)

        # Check if the correct logging level is set
        mock_logging.getLogger.assert_called()
        mock_logging.getLogger().setLevel.assert_called_with(mock_logging.INFO)

        # Check if the correct handlers are added
        mock_logging.FileHandler.assert_called_with('/path/to/log')
        mock_logging.StreamHandler.assert_called_with()

        # Check if the correct warnings are ignored
        mock_warnings.simplefilter.assert_any_call(action='ignore', category=FutureWarning)
        mock_warnings.simplefilter.assert_any_call(action='ignore', category=DeprecationWarning)

        # Check if the correct loggers are disabled
        mock_logging.getLogger.assert_any_call("scapy")
        mock_logging.getLogger.assert_any_call("torch")
        mock_logging.getLogger.assert_any_call("urllib3")
        mock_logging.getLogger.assert_any_call("requests")

    @mock.patch('pwnagotchi.log.logging')
    @mock.patch('pwnagotchi.log.warnings')
    def test_setup_logging_debug(self, mock_warnings, mock_logging):
        args = mock.Mock()
        args.debug = True
        config = {
            'main': {
                'log': {
                    'path': '/path/to/log',
                    'rotation': {
                        'enabled': True,  # or False, depending on your test case
                        # include other keys that log_rotation function might use
                }
                }
            }
        }

        setup_logging(args, config)

        # Check if the correct logging level is set
        mock_logging.getLogger.assert_called()
        mock_logging.getLogger().setLevel.assert_called_with(mock_logging.DEBUG)

        # Check if the correct handlers are added
        mock_logging.FileHandler.assert_called_with('/path/to/log')
        mock_logging.StreamHandler.assert_called_with()

        # Check if no warnings are ignored and no loggers are disabled
        mock_warnings.simplefilter.assert_not_called()
        mock_logging.getLogger().disabled.assert_not_called()

if __name__ == '__main__':
    unittest.main()