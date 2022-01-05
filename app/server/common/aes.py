from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


class AES128:
    _mode = AES.MODE_ECB
    _bs = 16

    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        raw = self._pad(raw)
        cipher = AES.new(self.key, self._mode)
        msg = cipher.encrypt(raw)
        return msg

    def decrypt(self, raw):
        cipher = AES.new(self.key, self._mode)
        plain = cipher.decrypt(raw)
        return self._unpad(plain)

    def _pad(self, s):
        return pad(s, self._bs)

    @staticmethod
    def _unpad(s):
        return s[: -ord(s[len(s) - 1 :])]

