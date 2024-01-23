import unittest
import sys
import os

# Get the directory of the current file and add it to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir + '/../')  # adjust this to the correct relative path

from pwnagotchi import _version

class TestVersion(unittest.TestCase):
    def test_version(self):
        self.assertEqual(_version.__version__, '0.2.0')

if __name__ == '__main__':
    unittest.main()