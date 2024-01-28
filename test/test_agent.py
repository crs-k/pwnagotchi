import unittest
from unittest.mock import patch, MagicMock, Mock
from pwnagotchi.agent import Agent
from pwnagotchi import utils

class TestAgent(unittest.TestCase):
    @patch('pwnagotchi.agent.AsyncAdvertiser')
    @patch('pwnagotchi.agent.Client')
    @patch('pwnagotchi.agent.Automata')
    
    @patch('pwnagotchi.agent.AsyncTrainer')
    @patch('pwnagotchi.agent.Server')
    @patch('pwnagotchi.agent.LastSession')
    @patch('pwnagotchi.utils.iface_channels', return_value=['1', '6', '11'])
    def setUp(self, mock_async_advertiser, mock_last_session, mock_server, mock_async_trainer, mock_automata, mock_client,mock_iface_channels):
        self.keypair = MagicMock()
        self.view = MagicMock()
        self.config = {
            'bettercap': {
                'hostname': 'localhost',
                'scheme': 'http',
                'port': 80,
                'username': 'pwnagotchi',
                'password': 'pwnagotchi',
                'handshakes': '/tmp/handshakes',
                'silence': ['tag1', 'tag2'] 
            },
            'main': {
                'iface': 'wlan0',
                'filter': None,
                'mon_start_cmd': 'start',
                'no_restart': False,
                'lang': 'en',
                'log': {
                    'path': '/path/to/log'  # Add this line
                }
            },
            'ui': {
                'display': {
                    'type': 'inky',
                    'color': 'black'
                },
                'web': {
                    'enabled': False,
                    'username': 'pwnagotchi',
                    'password': 'pwnagotchi',
                    'port': 8080,
                    'address': 'localhost'  

                }
            },
            'personality': {
                'recon_time': 30,
                'ap_ttl': 100,
                'sta_ttl': 200,
                'deauth': True,
                'associate': True,
                'handshakes': 50,
                'min_rssi': -70,
                'max_inactive_scale': 5,
                'recon_inactive_multiplier': 2,
                'channels': [1, 6, 11] 
            }
        }
        
        self.agent = Agent(self.view, self.config, self.keypair)
        self.agent.url = 'http://localhost:80/api'

    def test_config(self):
        self.assertEqual(self.agent.config(), self.config)

    def test_view(self):
        self.assertEqual(self.agent.view(), self.view)

    def test_supported_channels(self):
        self.agent._supported_channels = ['1', '6', '11']
        self.assertEqual(self.agent.supported_channels(), ['1', '6', '11'])

    @patch('pwnagotchi.logging')
    def test_setup_events(self, mock_logging):
        self.agent.run = MagicMock()
        self.agent.setup_events()
        self.agent.run.assert_called()

    @patch('pwnagotchi.logging')
    def test_reset_wifi_settings(self, mock_logging):
        self.agent.run = MagicMock()
        self.agent._reset_wifi_settings()
        self.agent.run.assert_called()

    @patch('pwnagotchi.logging')
    def test_start_monitor_mode(self, mock_logging):
        self.config['main']['no_restart'] = True  # Set to True
        self.agent.session = MagicMock(return_value={
        'interfaces': [
            {'name': self.config['main']['iface']}
            ]
        })
        self.agent.run = MagicMock()
        self.agent.is_module_running = MagicMock(return_value=False)  # Set return value to False
        self.agent.restart_module = MagicMock()
        self.agent.start_module = MagicMock()
        self.agent.start_advertising = MagicMock()
        self.agent.start_monitor_mode()
        self.agent.run.assert_called()
        self.agent.session.assert_called()
        self.agent.is_module_running.assert_called()
        #self.agent.restart_module.assert_called()
        self.agent.start_module.assert_called()
        self.agent.start_advertising.assert_called()

    @patch('pwnagotchi.logging')
    def test_start_monitor_mode_flipped(self, mock_logging):
        self.config['main']['no_restart'] = False
        self.agent.session = MagicMock(return_value={
        'interfaces': [
            {'name': self.config['main']['iface']}
            ]
        })
        self.agent.run = MagicMock()
        self.agent.is_module_running = MagicMock(return_value=True)  # Set return value to False
        self.agent.restart_module = MagicMock()
        self.agent.start_module = MagicMock()
        self.agent.start_advertising = MagicMock()
        self.agent.start_monitor_mode()
        self.agent.run.assert_called()
        self.agent.session.assert_called()
        self.agent.is_module_running.assert_called()
        self.agent.restart_module.assert_called()
        #self.agent.start_module.assert_called()
        self.agent.start_advertising.assert_called()
            
    @patch('pwnagotchi.logging')
    def test_wait_bettercap(self, mock_logging):
        self.agent.session = MagicMock()
        self.agent._wait_bettercap()
        self.agent.session.assert_called()

    @patch('pwnagotchi.agent.Agent.run')
    @patch('pwnagotchi.agent.Agent.wait_for')
    def test_recon(self, mock_run, mock_wait_for):
        self.agent._epoch = MagicMock()
        self.agent._epoch.inactive_for = 1
        self.agent._view = MagicMock()
        self.agent.recon()
        mock_run.assert_called_once()
        mock_wait_for.assert_called_once()

if __name__ == '__main__':
    unittest.main()