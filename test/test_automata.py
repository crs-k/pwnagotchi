import unittest
from unittest.mock import Mock, patch
from pwnagotchi.automata import Automata

class TestAutomata(unittest.TestCase):
    def setUp(self):
        self.config = {
            'personality': {
                'bond_encounters_factor': 1,
                'bored_num_epochs': 1,
                'sad_num_epochs': 1,
                'max_misses_for_recon': 1,
                'excited_num_epochs': 1
            },
            'main': {
                'mon_max_blind_epochs': 1
            }
        }
        self.view = Mock()
        self.automata = Automata(self.config, self.view)
        self.automata._peers = {}

    def test_set_starting(self):
        self.automata.set_starting()
        self.view.on_starting.assert_called_once()

    def test_set_ready(self):
        with patch('pwnagotchi.plugins.on') as mock_on:
            self.automata.set_ready()
            mock_on.assert_called_once_with('ready', self.automata)

    def test_set_grateful(self):
        with patch('pwnagotchi.plugins.on') as mock_on:
            self.automata.set_grateful()
            self.view.on_grateful.assert_called_once()
            mock_on.assert_called_once_with('grateful', self.automata)

    def test_set_lonely(self):
        with patch('pwnagotchi.plugins.on') as mock_on:
            self.automata.set_lonely()
            self.view.on_lonely.assert_called_once()
            mock_on.assert_called_once_with('lonely', self.automata)

    def test_set_bored(self):
        with patch('pwnagotchi.plugins.on') as mock_on:
            self.automata._epoch.inactive_for = 10
            self.automata._config['personality']['bored_num_epochs'] = 5
            self.automata._peers = {'peer1': Mock(encounters=1), 'peer2': Mock(encounters=1)}
            self.automata._config['personality']['bond_encounters_factor'] = 10
            self.automata.set_bored()
            self.view.on_bored.assert_called_once()
            mock_on.assert_called_once_with('bored', self.automata)

    def test_set_sad(self):
        with patch('pwnagotchi.plugins.on') as mock_on:
            self.automata._epoch.inactive_for = 10
            self.automata._config['personality']['sad_num_epochs'] = 5
            self.automata._peers = {'peer1': Mock(encounters=1), 'peer2': Mock(encounters=1)}
            self.automata._config['personality']['bond_encounters_factor'] = 10
            self.automata.set_sad()
            self.view.on_sad.assert_called_once()
            mock_on.assert_called_once_with('sad', self.automata)

    def test_set_angry(self):
        with patch('pwnagotchi.plugins.on') as mock_on:
            self.automata.set_angry(1.0)
            self.view.on_angry.assert_called_once()
            mock_on.assert_called_once_with('angry', self.automata)

    def test_set_excited(self):
        with patch('pwnagotchi.plugins.on') as mock_on:
            self.automata.set_excited()
            self.view.on_excited.assert_called_once()
            mock_on.assert_called_once_with('excited', self.automata)

    def test_set_rebooting(self):
        with patch('pwnagotchi.plugins.on') as mock_on:
            self.automata.set_rebooting()
            self.view.on_rebooting.assert_called_once()
            mock_on.assert_called_once_with('rebooting', self.automata)

    def test_wait_for(self):
        with patch('pwnagotchi.plugins.on') as mock_on:
            self.automata.wait_for(1)
            self.view.wait.assert_called_once_with(1, True)
            mock_on.assert_called_once_with('sleep', self.automata, 1)

    def test_is_stale(self):
        self.automata._epoch.num_missed = 2
        self.assertTrue(self.automata.is_stale())

    def test_any_activity(self):
        self.automata._epoch.any_activity = True
        self.assertTrue(self.automata.any_activity())

    def test_on_miss(self):
        with patch('pwnagotchi.plugins.on') as mock_on, \
            patch.object(self.automata._epoch, 'track') as mock_track:
            who = 'test'
            self.automata._on_miss(who)
            mock_track.assert_called_once_with(miss=True)
            self.automata._view.on_miss.assert_called_once_with(who)

    def test_on_error(self):
        with patch.object(self.automata, '_on_miss') as mock_on_miss:
            who = 'test'
            e = 'is an unknown BSSID'
            self.automata._on_error(who, e)
            mock_on_miss.assert_called_once_with(who)

    def test_in_good_mood(self):
        with patch.object(self.automata, '_has_support_network_for') as mock_has_support:
            mock_has_support.return_value = True
            assert self.automata.in_good_mood() == True
            mock_has_support.assert_called_once_with(1.0)

    @patch('pwnagotchi.temperature', return_value=50)
    def test_next_epoch(self, mock_temperature):
        with patch('pwnagotchi.plugins.on') as mock_on, \
            patch.object(self.automata, 'set_angry') as mock_set_angry:
            self.automata._epoch.num_missed = 10
            self.automata._config['personality']['max_misses_for_recon'] = 5
            self.automata.next_epoch()
            mock_set_angry.assert_called_once()
            mock_on.assert_called_once_with('epoch', self.automata, self.automata._epoch.epoch - 1, self.automata._epoch.data())

if __name__ == '__main__':
    unittest.main()