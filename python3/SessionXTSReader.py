#!/usr/bin/env python3
import sys, zipfile, configparser, base64
from Crypto.Hash import MD5
from Crypto.Cipher import ARC4
from XmanagerCrypto import *

XTSKey = MD5.new(b'!X@s#c$e%l^l&').digest()

def XTSEncryptString(s : str):
    cipher = ARC4.new(XTSKey)
    ciphertext = cipher.encrypt(s.encode())
    checksum = MD5.new(s.encode()).digest()
    return base64.b64encode(ciphertext + checksum).decode()

def XTSDecryptString(s : str):
    cipher = ARC4.new(XTSKey)
    data = base64.b64decode(s)
    ciphertext, checksum = data[:-MD5.digest_size], data[-MD5.digest_size:]
    plaintext = cipher.decrypt(ciphertext)
    assert(MD5.new(plaintext).digest() == checksum)
    return plaintext.decode()

def XTSGetUserName(Config : configparser.ConfigParser):
    try:
        return Config['SessionInfo']['UN']
    except:
        return None

def XTSGetComputerName(Config : configparser.ConfigParser):
    try:
        return Config['SessionInfo']['CN']
    except:
        return None

def XTSGetSID(Config : configparser.ConfigParser):
    try:
        return Config['SessionInfo']['SI']
    except:
        return None

def XTSPrintXShellSession(Config : configparser.ConfigParser, username : str, sid : str, masterpwd : str):
    Version = Config['SessionInfo']['Version']
    Host = Config['CONNECTION']['Host']
    Port = Config['CONNECTION']['Port']
    Username = Config['CONNECTION:AUTHENTICATION']['UserName']
    Password = Config['CONNECTION:AUTHENTICATION']['Password']

    cipher = XShellCrypto(Version, UserName = username, SID = sid, MasterPassword = masterpwd)
    try:
        DecryptedPassword = cipher.DecryptString(Password)
        Password = DecryptedPassword
    except:
        pass
    
    print('%-12s = %s' % ('Host', Host))
    print('%-12s = %s' % ('Port', Port))
    print('%-12s = %s' % ('UserName', Username))
    print('%-12s = %s' % ('Password', Password))

def XTSPrintXFtpSession(Config : configparser.ConfigParser, username : str, sid : str, masterpwd : str):
    Version = Config['SessionInfo']['Version']
    Host = Config['Connection']['Host']
    Port = Config['Connection']['Port']
    Username = Config['Connection']['UserName']
    Password = Config['Connection']['Password']

    cipher = XFtpCrypto(Version, UserName = username, SID = sid, MasterPassword = masterpwd)
    try:
        DecryptedPassword = cipher.DecryptString(Password)
        Password = DecryptedPassword
    except:
        pass

    print('%-12s = %s' % ('Host', Host))
    print('%-12s = %s' % ('Port', Port))
    print('%-12s = %s' % ('UserName', Username))
    print('%-12s = %s' % ('Password', Password))

def TryDecode(b : bytes):
    try:
        return b.decode()
    except:
        pass
    
    try:
        return b.decode('utf16')
    except:
        pass

    raise UnicodeDecodeError('Cannot decode for unknown encoding.')

def main(XTSFilePath : str, UserName, ComputerName, SID, MasterPassword):
    with zipfile.ZipFile(XTSFilePath) as XTSFile:
        config = configparser.ConfigParser()
        config.read_string(TryDecode(XTSFile.read('xts.zcf')))

        if UserName == None:
            UserName = XTSGetUserName(config)
            if UserName != None and len(UserName) != 0:
                UserName = XTSDecryptString(UserName)
        if ComputerName == None:
            ComputerName = XTSGetComputerName(config)
            if ComputerName != None and len(ComputerName) != 0:
                ComputerName = XTSDecryptString(ComputerName)
        if SID == None:
            SID = XTSGetSID(config)
            if SID != None and len(SID) != 0:
                SID = XTSDecryptString(SID)
        
        if ComputerName != None and len(ComputerName) != 0:
            print('%-12s = %s' % ('ComputerName', ComputerName))
        if UserName != None and len(UserName) != 0:
            print('%-12s = %s' % ('UserName', UserName))
        if SID != None and len(SID) != 0:
            print('%-12s = %s' % ('SID', SID))
        if MasterPassword != None and len(MasterPassword) != 0:
            print('%-12s = %s' % ('MasterPwd', MasterPassword))

        print()

        for File in XTSFile.infolist():
            if File.flag_bits & 0x800:
                FileName = File.filename
            else:
                try:
                    FileName = File.filename.encode('cp437').decode('ansi')
                except:
                    FileName = File.filename
            
            FileNameL = FileName.lower()
            if FileNameL == 'xts.zcf':
                continue
            
            if FileNameL.startswith('xshell/') and FileNameL.endswith('.xsh'):
                config.clear()
                config.read_string(TryDecode(XTSFile.read(File.filename)))
                print(FileName)
                XTSPrintXShellSession(config, UserName, SID, MasterPassword)
            elif FileNameL.startswith('xftp/') and FileNameL.endswith('.xfp'):
                config.clear()
                config.read_string(TryDecode(XTSFile.read(File.filename)))
                print(FileName)
                XTSPrintXFtpSession(config, UserName, SID, MasterPassword)
                print()
            else:
                if File.is_dir() == False:
                    print('Unhandled file: %s' % File.filename)
                continue
            print()

def help():
    print('Usage:')
    print('    SessionXTSReader.py [-user user_string]')
    print('                        [-sid  sid_string]')
    print('                        [-key  key_string]')
    print('                        <XTS file path>')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        help()
        exit(0)
    
    user = None
    sid = None
    key = None
    path = None

    i = 1
    while i < len(sys.argv):
        if sys.argv[i].lower() == '-user':
            user = sys.argv[i + 1]
            i += 1
        elif sys.argv[i].lower() == '-sid':
            sid = sys.argv[i + 1]
            i += 1
        elif sys.argv[i].lower() == '-key':
            key = sys.argv[i + 1]
            i += 1
        else:
            path = sys.argv[i]
            break
        i += 1
    
    main(path, user, None, sid, key)
else:
    print('Please run as script directly')
