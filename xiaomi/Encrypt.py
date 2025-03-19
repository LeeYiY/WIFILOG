import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import time
import random

class Encrypt:
    def __init__(self):
        self.key = 'a2ffa5c9be07488bbb04a3a47d3c5f6a'
        self.iv = '64175472480004614961023454661220'
        self.nonce = None

    def init(self):
        nonce = self.nonceCreat()
        self.nonce = nonce
        return self.nonce

    def nonceCreat(self):
        type_ = 0
        device_id = 'e0:be:03:1f:32:4e'
        current_time = int(time.time())
        random_num = random.randint(0, 9999)
        return f"{type_}_{device_id}_{current_time}_{random_num}"

    def oldPwd(self, pwd):
        first_sha1 = hashlib.sha1((pwd + self.key).encode()).hexdigest()
        combined = self.nonce + first_sha1
        return hashlib.sha1(combined.encode()).hexdigest()

