import unittest
from unittest.mock import patch, MagicMock
from packaging.version import parse as parse_version
import os
import sys

def convert_version(version):
    converted_version = parse_version(version)
    return converted_version

class TestUpdateCheck(unittest.TestCase):
    def test_update_available(self):
        local = convert_version('v0.7.0')
        remote = convert_version('v0.6.0')

        if remote > local:
            print("remote is greater than local")
            if 'y' in ('y', 'yes'):
                if os.path.exists('/root/.auto-update'):
                   print("yes was selected")
                else:
                    print("You should make sure auto-update is enabled!")
                print("Check pwnlog for updates.")
            elif 'n' in ('n', 'no'):
                print("Update cancelled.")
        else:
            print("You are currently on the latest release, v%s." % local)

if __name__ == '__main__':
    unittest.main()