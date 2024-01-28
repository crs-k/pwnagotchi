import tempfile
import unittest
from unittest.mock import MagicMock, patch
import os
import subprocess
from pwnagotchi.identity import KeyPair

class TestKeyPair(unittest.TestCase):
    def setUp(self):
        test_dir = os.path.dirname(os.path.abspath(__file__))  # Get the path of the current file (test_identity.py)
        self.temp_dir = tempfile.TemporaryDirectory(dir=test_dir)  # Create the temporary directory in the test directory
        self.view_mock = MagicMock()
        # Run the gen_testkey.py script to generate the keys
        gen_testkey_path = os.path.join(test_dir, 'gen_testkey.py')  # Get the absolute path to the gen_testkey.py script
        subprocess.run(['python3', gen_testkey_path, self.temp_dir.name])
        self.key_pair = KeyPair(path=self.temp_dir.name, view=self.view_mock)



    def test_one_equals_one(self):
        self.assertEqual(1, 1)

    @patch('os.system')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('os.remove')
    @patch('shutil.copy')
    @patch('logging.warning')
    @patch('logging.info')
    @patch('logging.exception')
    def test_init(self, log_exception_mock, log_info_mock, log_warning_mock, shutil_copy_mock, os_remove_mock, os_makedirs_mock, os_path_exists_mock, os_system_mock):
        # Define a side effect function that returns True for backup files and False for other files
        def side_effect(arg):
            if arg in [self.key_pair.priv_path, self.key_pair.pub_path, f'{self.key_pair.priv_path}.original', f'{self.key_pair.pub_path}.original', f'{self.key_pair.fingerprint_path}.original']:
                return False
            else:
                return True

        # Set the side effect function for the os.path.exists mock
        os_path_exists_mock.side_effect = side_effect

        # Create a KeyPair object
        key_pair = KeyPair(path=self.temp_dir.name, view=self.view_mock)

        # Check that the keys were generated
        os_system_mock.assert_called_once_with("pwngrid -generate -keys '%s'" % self.temp_dir.name)

        # Check that the keys were loaded
        self.assertIsNotNone(key_pair.priv_key)
        self.assertIsNotNone(key_pair.pub_key)

        # Check that the keys were backed up
        self.assertEqual(shutil_copy_mock.call_count, 3)

    @patch('os.system')
    @patch('os.path.exists')
    def test_generate_keys(self, os_path_exists_mock, mock_system):
        # Define a side effect function that returns False for the keys and the backup files
        def side_effect(arg):
            if arg in [self.key_pair.priv_path, self.key_pair.pub_path, f'{self.key_pair.priv_path}.original', f'{self.key_pair.pub_path}.original', f'{self.key_pair.fingerprint_path}.original']:
                return False
            else:
                return True

        # Set the side effect function for the os.path.exists mock
        os_path_exists_mock.side_effect = side_effect

        self.key_pair = KeyPair(path=self.temp_dir.name, view=self.view_mock)
        self.assertTrue(os.path.exists(self.key_pair.path))
        mock_system.assert_called_once()

    @unittest.mock.patch('os.remove')
    @unittest.mock.patch('Crypto.Signature.pss.new', side_effect=AttributeError)
    def test_exception_handling(self, mock_remove, mock_pss_new):
        with self.assertRaises(AttributeError):
            self.key_pair.sign('test message')
        mock_remove.assert_called()

    def test_sign(self):
        # This test assumes that the keys are correctly generated and loaded.
        # You may need to adjust this depending on how your keys are set up.
        message = 'test message'
        signature, signature_b64 = self.key_pair.sign(message)
        self.assertIsNotNone(signature)
        self.assertIsNotNone(signature_b64)

    def tearDown(self):
        self.temp_dir.cleanup()

if __name__ == '__main__':
    unittest.main()