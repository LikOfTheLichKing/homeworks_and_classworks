import hashlib
import base64
import random

class PasswordHandler():
    def __init__(self, password: str, pepper: str|None, hash_method, encode_method):
        """
        hash_method: put a link to the hash function
        encode_method: put a link to the encode function
        """
        if pepper is None:
            self.password = password
        else:
            self.password = password+pepper
        self.hash = hash_method
        self.encode = encode_method

    def hash_password_raw(self, password: str) -> str:
        hash_data = self.hash(password.encode("utf-8"))
        return self.encode(hash_data.digest()).decode("utf-8")

    def hash_password(self) -> str:
        salt = self.get_salt()
        return self.hash_password_raw(self.password + ":" + salt) + ":" + salt

    def get_salt(self) -> str:
        salt_number = random.randint(0, 2 ** 256 - 1)
        return self.encode(salt_number.to_bytes(32, "little")).decode("utf-8")

    def passwords_equal(self, hash: str) -> bool:
        raw_hash, salt = hash.split(":", 2)
        return self.hash_password() + ":" + salt == raw_hash

password = PasswordHandler(password="1234", hash_method=hashlib.sha512, encode_method=base64.b32encode)
print(password.hash_password())
