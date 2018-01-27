from XmanagerCrypto import *
import sys

def Help():
    print('Usage:')
    print('    XmanagerCryptoHelper.py <-e|-d> <password_str|base64_str>')

if __name__ == '__main__':
    Cipher = XmanagerCrypto()
	
    if len(sys.argv) == 3:
        if sys.argv[1] == '-d':
            print(Cipher.DecryptString(sys.argv[2]))
        elif sys.argv[1] == '-e':
            print(Cipher.EncryptString(sys.argv[2]))
        else:
            Help()
    else:
        Help()
	
    print()
	