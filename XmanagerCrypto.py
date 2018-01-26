import win32api
import win32security
import base64
import sys
from Crypto.Cipher import ARC4
from Crypto.Hash import SHA256

def DecryptString(cipher : ARC4, s : str):
    data = base64.b64decode(s)
    checksum = data[-32:]
    ciphertext = data[0:-32]
    plaintext = cipher.decrypt(ciphertext)

    assert SHA256.new(plaintext).digest() == checksum
    return plaintext.decode()

def EncryptString(cipher : ARC4, s : str):
    plaintext = s.encode()
    checksum = SHA256.new(plaintext).digest()
    ciphertext = cipher.encrypt(plaintext)

    return base64.b64encode(ciphertext + checksum).decode()

def Help():
    print('Usage:')
    print('    XmanagerCrypto.py <-e|-d> <pwd_string|encrypted_pwd_base64string>')
    print()

CurrentUserName = win32api.GetUserName()
CurrentComputerName = win32api.GetComputerName()
CurrentUserSID = win32security.LookupAccountName(CurrentComputerName, CurrentUserName)[0]
CurrentuserSIDString = win32security.ConvertSidToStringSid(CurrentUserSID)

key = (CurrentUserName + CurrentuserSIDString).encode()
cipher_key = SHA256.new(key).digest()

cipher = ARC4.new(cipher_key)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        if sys.argv[1] == '-d':
            print(DecryptString(cipher, sys.argv[2]))
            print()
        elif sys.argv[1] == '-e':
            print(EncryptString(cipher, sys.argv[2]))
            print()
        else:
            Help()
    else:
        Help()
