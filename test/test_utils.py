import unittest
from pwnagotchi.utils import DottedTomlEncoder, total_unique_handshakes, iface_channels, led, md5, blink, secs_to_hhmmss, load_config, convert_version, remove_whitelisted, download_file, unzip, merge_config, keys_to_str, save_config
import os
import toml
from unittest.mock import patch, mock_open
from packaging.version import Version

class TestUtils(unittest.TestCase):
    def test_convert_version(self):
        self.assertEqual(convert_version('1.2.3'), Version('1.2.3'))

    def test_remove_whitelisted(self):
        handshakes = ['test1.pcap', 'test2.pcap', 'test3.pcap']
        whitelisted = ['test1', 'test3']
        self.assertEqual(remove_whitelisted(handshakes, whitelisted), ['test2.pcap'])

    def test_merge_config(self):
        user = {'key1': 'value1', 'key2': 'value2'}
        default = {'key2': 'default_value2', 'key3': 'default_value3'}
        self.assertEqual(merge_config(user, default), {'key1': 'value1', 'key2': 'value2', 'key3': 'default_value3'})

    def test_keys_to_str(self):
        data = {'key1': 'value1', 2: 'value2'}
        self.assertEqual(keys_to_str(data), {'key1': 'value1', '2': 'value2'})

    def test_save_config(self):
        config = {'key1': 'value1', 'key2': 'value2'}
        target = 'test.toml'
        save_config(config, target)
        with open(target, 'r') as file:
            data = toml.load(file)
        self.assertEqual(data, config)
        os.remove(target)

    @patch('builtins.open', new_callable=mock_open, read_data='main = { "confd": "/path/to/confd" }\nui = { "display": { "type": "inky" } }')
    @patch('shutil.move')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('os.path.isdir')
    @patch('shutil.copy')
    @patch('toml.load')
    def test_load_config(self, mock_toml_load, mock_shutil_copy, mock_os_isdir, mock_os_makedirs, mock_os_exists, mock_shutil_move, mock_open):
        class Args:
            def __init__(self):
                self.config = '/path/to/config'
                self.user_config = '/path/to/user_config'

        args = Args()

        # Mock the shutil.move function to do nothing
        mock_shutil_move.side_effect = lambda x, y: None


        # Mock the os.path.exists function to always return True
        mock_os_exists.return_value = True

        # Mock the os.makedirs function to do nothing
        mock_os_makedirs.side_effect = lambda x: None

        # Mock the os.path.isdir function to always return True
        mock_os_isdir.return_value = True

        # Mock the shutil.copy function to do nothing
        mock_shutil_copy.side_effect = lambda x, y: None

        # Mock the toml.load function to return a dictionary
        mock_toml_load.return_value = {
            'main': {'confd': '/path/to/confd'},
            'ui': {'display': {'type': 'inky'}}
        }

        config = load_config(args)

        self.assertEqual(config['ui']['display']['type'], 'inky')

    def test_secs_to_hhmmss(self):
        self.assertEqual(secs_to_hhmmss(3661), '01:01:01')

    @patch('os.path.join')
    @patch('glob.glob')
    def test_total_unique_handshakes(self, mock_glob, mock_join):
        mock_glob.return_value = ['file1', 'file2', 'file3']
        self.assertEqual(total_unique_handshakes('path'), 3)

    @patch('subprocess.getoutput')
    def test_iface_channels(self, mock_getoutput):
        mock_getoutput.side_effect = ['0', '1\n2\n3']
        self.assertEqual(iface_channels('ifname'), [1, 2, 3])

    @patch('builtins.open', new_callable=mock_open)
    def test_led(self, mock_open):
        led(True)
        mock_open().write.assert_called_once_with('0')

    @patch('time.sleep')
    @patch('pwnagotchi.utils.led')
    def test_blink(self, mock_led, mock_sleep):
        blink(times=2, delay=0.1)
        self.assertEqual(mock_led.call_count, 5)

if __name__ == '__main__':
    unittest.main()