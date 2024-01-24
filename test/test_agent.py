import unittest
from unittest.mock import patch, MagicMock
from pwnagotchi.agent import Agent

class TestAgent(unittest.TestCase):
    @patch('pwnagotchi.utils.iface_channels', return_value=[1, 2, 3, 4, 5, 6, 9, 10, 11, 13])
   # def setUp(self, mock_iface_channels):
       # self.agent = Agent(self.view, self.config, self.keypair)
    @patch('pwnagotchi.agent.Client')
    @patch('pwnagotchi.agent.Automata')
    @patch('pwnagotchi.agent.AsyncAdvertiser')
    @patch('pwnagotchi.agent.AsyncTrainer')
    def setUp(self, mock_iface_channels, MockClient, MockAutomata, MockAsyncAdvertiser, MockAsyncTrainer):
        self.view = MagicMock()
        self.config = {
            'bettercap': {
                'hostname': 'localhost',
                'scheme': 'http',
                'port': 60,
                'username': 'admin',
                'password': 'admin',
                'handshakes': '/tmp/handshakes'
            },
            'main': {
                'filter': None,
                'iface': 'wlan0',
                'mon_start_cmd': None,
                'no_restart': False
            },
            'personality': {
                'ap_ttl': 60,
                'sta_ttl': 60,
                'min_rssi': -80,
                'recon_time': 30,
                'max_inactive_scale': 300,
                'recon_inactive_multiplier': 2,
                'channels': [
                            1,
                            2,
                            3,
                            4,
                            5,
                            6,
                            9,
                            10,
                            11,
                            13,
                            ]
            },
            
            'ui': {'web': {'enabled': True,
                           'address': "0.0.0.0",
                           'username': "pwnagotchi",
                           'password': "pwnagotchi",
                           'origin': "",
                           'port': 8080,
                           'on_frame': ""}}
        }
        self.keypair = MagicMock()
        self.agent = Agent(self.view, self.config, self.keypair)

    def test_config(self):
        self.assertEqual(self.agent.config(), self.config)

    def test_view(self):
        self.assertEqual(self.agent.view(), self.view)

    def test_supported_channels(self):
        # Assuming utils.iface_channels returns [1, 6, 11] for 'wlan0'
        self.assertEqual(self.agent.supported_channels(), [1, 6, 11])

    @patch('pwnagotchi.agent.logging')
    def test_setup_events(self, mock_logging):
        self.agent.run = MagicMock()
        self.agent.setup_events()
        self.agent.run.assert_called()

    @patch('pwnagotchi.agent.logging')
    def test_reset_wifi_settings(self, mock_logging):
        self.agent.run = MagicMock()
        self.agent._reset_wifi_settings()
        self.agent.run.assert_called()

    @patch('pwnagotchi.agent.logging')
    def test_start_monitor_mode(self, mock_logging):
        self.agent.run = MagicMock()
        self.agent.session = MagicMock()
        self.agent._reset_wifi_settings = MagicMock()
        self.agent.is_module_running = MagicMock()
        self.agent.restart_module = MagicMock()
        self.agent.start_module = MagicMock()
        self.agent.start_advertising = MagicMock()
        self.agent.start_monitor_mode()
        self.agent.run.assert_called()

    @patch('pwnagotchi.agent.logging')
    def test_wait_bettercap(self, mock_logging):
        self.agent.session = MagicMock()
        self.agent._wait_bettercap()
        self.agent.session.assert_called()

    @patch('pwnagotchi.agent.logging')
    def test_start(self, mock_logging):
        self.agent.start_ai = MagicMock()
        self.agent._wait_bettercap = MagicMock()
        self.agent.setup_events = MagicMock()
        self.agent.set_starting = MagicMock()
        self.agent.start_monitor_mode = MagicMock()
        self.agent.start_event_polling = MagicMock()
        self.agent.start_session_fetcher = MagicMock()
        self.agent.next_epoch = MagicMock()
        self.agent.set_ready = MagicMock()
        self.agent.start()
        self.agent.start_ai.assert_called()

    @patch('pwnagotchi.agent.logging')
    def test_recon(self, mock_logging):
        self.agent.run = MagicMock()
        self.agent._epoch = MagicMock()
        self.agent._epoch.inactive_for = 0
        self.agent._view = MagicMock()
        self.agent.recon()
        self.agent.run.assert_called()

if __name__ == '__main__':
    unittest.main()