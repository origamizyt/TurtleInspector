import base64, os, sys
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, SHA384
from Crypto.Util import Padding

KEY_SIZE = 32

if sys.version_info >= (3, 8):
    def ashex(data: bytes, sep: str='', count: int=1):
        'Converts bytes to hex with separator and byte count.'
        return data.hex(sep, count)
else:
    def ashex(data: bytes, sep: str='', count: int=1):
        'Converts bytes to hex with separator and byte count.'
        hexed = data.hex()
        return sep.join(data[i:i+count*2] for i in range(0, len(data), count*2))

def encode_base64(data: bytes) -> str:
    'Encodes bytes data as base-64 string.'
    return base64.b64encode(data).decode()

def decode_base64(data: str) -> bytes:
    'Decodes base-64 string as bytes data.'
    return base64.b64decode(data.encode())

class Key:
    'Represents a AES key.'
    def __init__(self, key: bytes):
        'Initializes a new instance with specific key.'
        self._key = key
    def sign(self, data: bytes) -> bytes:
        'Signs the data with the key.'
        cipher = AES.new(self._key, AES.MODE_ECB)
        encrypted = cipher.encrypt(Padding.pad(data, AES.block_size))
        return SHA384.new(encrypted).digest()
    def verify(self, data: bytes, signature: bytes) -> bool:
        'Verifies the data with the key.'
        return self.sign(data) == signature
    @property
    def token(self) -> str:
        'Represents the token of this key.'
        return self._key.hex()
    @property
    def fingerprint(self) -> str:
        'Represents the fingerprint of the key.'
        return ashex(SHA256.new(self._key).digest(), ':', 2)
    @staticmethod
    def fromToken(token: str) -> 'Key':
        'Generates a key from specific token.'
        return Key(bytes.fromhex(token))
    @staticmethod
    def generate() -> 'Key':
        'Generates a random key.'
        return Key(os.urandom(32))