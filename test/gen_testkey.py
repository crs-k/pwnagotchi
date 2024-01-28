from Crypto.Signature import PKCS1_PSS
from Crypto.PublicKey import RSA
import Crypto.Hash.SHA256 as SHA256
import base64
import hashlib
import os
import logging
import shutil
import sys


# Generate a new key pair
key = RSA.generate(2048)  # 2048 bits for production use

# Get the directory from the command line arguments
directory = sys.argv[1] if len(sys.argv) > 1 else '.'

# Save the keys in PEM format
with open(os.path.join(directory, 'id_rsa'), 'wb') as priv_file:
    priv_file.write(key.exportKey('PEM'))

with open(os.path.join(directory, 'id_rsa.pub'), 'wb') as pub_file:
    pub_file.write(key.publickey().exportKey('PEM'))