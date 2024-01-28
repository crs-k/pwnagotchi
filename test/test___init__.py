
import unittest
from unittest.mock import patch, mock_open
import pwnagotchi

class TestPwnagotchi(unittest.TestCase):
    def test_set_name(self):
        # Test with None
        self.assertIsNone(pwnagotchi.set_name(None))

        # Test with empty string
        self.assertIsNone(pwnagotchi.set_name(''))

        # Test with invalid name
        self.assertIsNone(pwnagotchi.set_name('invalid-name!'))

    @patch('builtins.open', new_callable=mock_open, read_data="test_name")
    def test_name(self, mock_file):
        self.assertEqual(pwnagotchi.name(), "test_name")
        mock_file.assert_called_with('/etc/hostname', 'rt')

    @patch('builtins.open', new_callable=mock_open, read_data="12345.67")
    def test_uptime(self, mock_file):
        self.assertEqual(pwnagotchi.uptime(), 12345)
        mock_file.assert_called_with('/proc/uptime')

    @patch('builtins.open', new_callable=mock_open, read_data="MemTotal: 2048\nMemFree: 1024\nBuffers: 512\nCached: 512")
    def test_mem_usage(self, mock_file):
        self.assertEqual(pwnagotchi.mem_usage(), 0.0)
        mock_file.assert_called_with('/proc/meminfo')

    # Fix for test_cpu_load
    def test_cpu_load(self):
        load = pwnagotchi.cpu_load()
        self.assertIsInstance(load, float)
        self.assertGreaterEqual(load, 0)
        self.assertLessEqual(load, 1)


    @patch('builtins.open', new_callable=mock_open, read_data="50000")
    def test_temperature(self, mock_file):
        self.assertEqual(pwnagotchi.temperature(), 50)
        mock_file.assert_called_with('/sys/class/thermal/thermal_zone0/temp', 'rt')

    # @patch('pwnagotchi.os.system')
    # @patch('pwnagotchi.logging')
    # def test_shutdown(self, mock_logging, mock_system):
    #     pwnagotchi.shutdown()
    #     mock_system.assert_any_call("sync")
    #     mock_system.assert_any_call("halt")
    #     mock_logging.warning.assert_called_with("shutting down ...")

    @patch('pwnagotchi.os.system')
    @patch('pwnagotchi.logging')
    def test_restart(self, mock_logging, mock_system):
        pwnagotchi.restart('auto')
        mock_system.assert_any_call("touch /root/.pwnagotchi-auto")
        mock_system.assert_any_call("service pwnagotchi restart")
        mock_logging.warning.assert_called_with("restarting in %s mode ...", 'auto')

    # @patch('pwnagotchi.os.system')
    # @patch('pwnagotchi.logging')
    # def test_reboot(self, mock_logging, mock_system):
    #     pwnagotchi.reboot('auto')
    #     mock_system.assert_any_call("touch /root/.pwnagotchi-auto")
    #     mock_system.assert_any_call("shutdown -r now")
    #     mock_logging.warning.assert_called_with("rebooting in %s mode ...", 'auto')

if __name__ == '__main__':
    unittest.main()