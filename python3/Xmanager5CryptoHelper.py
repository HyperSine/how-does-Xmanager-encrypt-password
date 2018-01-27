from XmanagerCrypto import *
import sys

def Help():
    print('Usage:')
    print('    Xmanager5CryptoHelper.py <-e|-d> <password_str|base64_str>')

if __name__ == '__main__':
    Cipher = Xmanager5Crypto()
	
    if len(sys.argv) == 3:
        if sys.argv[1] == '-d':
            print(Cipher.DecryptString2(sys.argv[2]))
        elif sys.argv[1] == '-e':
            print(Cipher.EncryptString2(sys.argv[2]))
        else:
            Help()
    else:
        Help()
	
    print()
	