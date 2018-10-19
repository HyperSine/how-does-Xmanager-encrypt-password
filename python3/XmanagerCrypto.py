#!/usr/bin/env python3
from base64 import b64encode, b64decode
from Crypto.Hash import MD5, SHA256
from Crypto.Cipher import ARC4

class XShellCrypto(object):

    def __init__(self, SessionFileVersion = 0xffff, **kwargs):
        '''
        SessionFileVersion must be convertable to float

        Supported kwargs:
            UserName : str
            SID : str
            MasterPassword : str
        '''
        self._Version = float(SessionFileVersion)
        if 0 < self._Version and self._Version < 5.1:
            self._Key = MD5.new(b'!X@s#h$e%l^l&').digest()
        elif 5.1 <= self._Version and self._Version <= 5.2:
            self._Key = SHA256.new(kwargs['SID'].encode()).digest()
        elif 5.2 < self._Version:
            if kwargs.get('MasterPassword') == None:
                self._Key = SHA256.new((kwargs['UserName'] + kwargs['SID']).encode()).digest()
            else:
                self._Key = SHA256.new(kwargs['MasterPassword'].encode()).digest()
        else:
            raise ValueError('Invalid argument: SessionFileVersion')

    def EncryptString(self, String : str):
        Cipher = ARC4.new(self._Key)
        if self._Version < 5.1:
            return b64encode(Cipher.encrypt(String.encode())).decode()
        else:
            checksum = SHA256.new(String.encode()).digest()
            ciphertext = Cipher.encrypt(String.encode())
            return b64encode(ciphertext + checksum).decode()
        

    def DecryptString(self, String : str):
        Cipher = ARC4.new(self._Key)
        if self._Version < 5.1:
            return Cipher.decrypt(b64decode(String)).decode()
        else:
            data = b64decode(String)
            ciphertext, checksum = data[:-SHA256.digest_size], data[-SHA256.digest_size:]
            plaintext = Cipher.decrypt(ciphertext)
            if SHA256.new(plaintext).digest() != checksum:
                raise ValueError('Cannot decrypt string. The key is wrong!')
            return plaintext.decode()

class XFtpCrypto(object):

    def __init__(self, SessionFileVersion = 0xffff, **kwargs):
        '''
        SessionFileVersion must be convertable to float

        Supported kwargs:
            UserName : str
            SID : str
            MasterPassword : str
        '''
        self._Version = float(SessionFileVersion)
        if 0 < self._Version and self._Version < 5.1:
            self._Key = MD5.new(b'!X@s#c$e%l^l&').digest()      # key is different with the one in XShellCrypto
        elif 5.1 <= self._Version and self._Version <= 5.2:
            self._Key = SHA256.new(kwargs['SID'].encode()).digest()
        elif 5.2 < self._Version:
            if kwargs.get('MasterPassword') == None:
                self._Key = SHA256.new((kwargs['UserName'] + kwargs['SID']).encode()).digest()
            else:
                self._Key = SHA256.new(kwargs['MasterPassword'].encode()).digest()
        else:
            raise ValueError('Invalid argument: SessionFileVersion')

    def EncryptString(self, String : str):
        Cipher = ARC4.new(self._Key)
        if self._Version < 5.1:
            return b64encode(Cipher.encrypt(String.encode())).decode()
        else:
            checksum = SHA256.new(String.encode()).digest()
            ciphertext = Cipher.encrypt(String.encode())
            return b64encode(ciphertext + checksum).decode()
        

    def DecryptString(self, String : str):
        Cipher = ARC4.new(self._Key)
        if self._Version < 5.1:
            return Cipher.decrypt(b64decode(String)).decode()
        else:
            data = b64decode(String)
            ciphertext, checksum = data[:-SHA256.digest_size], data[-SHA256.digest_size:]
            plaintext = Cipher.decrypt(ciphertext)
            if SHA256.new(plaintext).digest() != checksum:
                raise ValueError('Cannot decrypt string. The key is wrong!')
            return plaintext.decode()

