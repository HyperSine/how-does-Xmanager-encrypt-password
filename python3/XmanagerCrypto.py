import win32api
import win32security
import base64
from Crypto.Hash import MD5, SHA256
from Crypto.Cipher import ARC4

class XmanagerCrypto:

    def __init__(self):
        self.Key = b'!X@s#h$e%l^l&'

    def EncryptString(self, s : str):
        Cipher = ARC4.new(MD5.new(self.Key).digest())
        return base64.b64encode(Cipher.encrypt(s.encode())).decode()

    def DecryptString(self, s : str):
        Cipher = ARC4.new(MD5.new(self.Key).digest())
        return Cipher.decrypt(base64.b64decode(s)).decode()

class Xmanager5Crypto:

    def __init__(self, username = '', usersid = ''):
        if username == '' and usersid == '':
            self.UserName = win32api.GetUserName()
            CurrentUserSID = win32security.LookupAccountName(win32api.GetComputerName(), self.UserName)[0]
            self.UserSID = win32security.ConvertSidToStringSid(CurrentUserSID)
        else:
            self.UserName = str(username)
            self.UserSID = str(usersid)

    def EncryptString(self, s : str):
        Cipher = ARC4.new(SHA256.new(self.UserSID.encode()).digest())

        Plaintext = s.encode()
        Checksum = SHA256.new(Plaintext).digest()
        Ciphertext = Cipher.encrypt(Plaintext)

        return base64.b64encode(Ciphertext + Checksum).decode()

    def DecryptString(self, s : str):
        Cipher = ARC4.new(SHA256.new(self.UserSID.encode()).digest())

        Data = base64.b64decode(s)
        Checksum = Data[-32:]
        Ciphertext = Data[0:-32]
        Plaintext = Cipher.decrypt(Ciphertext)

        assert SHA256.new(Plaintext).digest() == Checksum
        return Plaintext.decode()

    def EncryptString2(self, s: str):
        Cipher = ARC4.new(SHA256.new((self.UserName + self.UserSID).encode()).digest())

        Plaintext = s.encode()
        Checksum = SHA256.new(Plaintext).digest()
        Ciphertext = Cipher.encrypt(Plaintext)

        return base64.b64encode(Ciphertext + Checksum).decode()

    def DecryptString2(self, s : str):
        Cipher = ARC4.new(SHA256.new((self.UserName + self.UserSID).encode()).digest())

        Data = base64.b64decode(s)
        Checksum = Data[-32:]
        Ciphertext = Data[0:-32]
        Plaintext = Cipher.decrypt(Ciphertext)

        assert SHA256.new(Plaintext).digest() == Checksum
        return Plaintext.decode()
