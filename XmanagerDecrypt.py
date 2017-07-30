import win32api
import win32security
import base64
from Crypto.Hash import SHA256
from Crypto.Cipher import ARC4

userSIDString = input('Input SID or leave it empty and the current account\'s SID will be used:')
if(userSIDString == ''):
    CurrentUserName = win32api.GetUserName()
    CurrentComputerName = win32api.GetComputerName()
    userSID = win32security.LookupAccountName(CurrentComputerName, CurrentUserName)[0]
    userSIDString = win32security.ConvertSidToStringSid(userSID)

encrypted_password = input('Input encrypted password (in Base64 format):')
encrypted_password = base64.b64decode(encrypted_password)
sha256_of_password = encrypted_password[-32:]
encrypted_password = encrypted_password[0 : len(encrypted_password) - 32]

key = SHA256.new(userSIDString.encode('ascii')).digest()
rc4_cipher = ARC4.new(key)
password = rc4_cipher.decrypt(encrypted_password)

if SHA256.new(password).digest() == sha256_of_password:
    print(password.decode('ascii'))
else:
    print('Failed to decrypt.')