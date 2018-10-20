#!/usr/bin/env python3
import sys
from XmanagerCrypto import XFtpCrypto

def GetCurrentUserName():
    import win32api
    return win32api.GetUserName()

def GetCurrentSID():
    import win32api, win32security
    Sid = win32security.LookupAccountName(win32api.GetComputerName(), win32api.GetUserName())[0]
    return win32security.ConvertSidToStringSid(Sid)

def help():
    print('Usage:')
    print('    XFtpCryptoHelper.py <-e | -d>')
    print('                        [-ver    ver_sting]')
    print('                        [-user   user_string]') 
    print('                        [-sid    sid_string]')
    print('                        [-key    key_string]')
    print('                        <password_str | base64_str>')
    print('')
    print('    <-e|-d>:                     Specify encryption(-e) or decryption(-d).')
    print('')
    print('    [-ver ver_string]:           Specify version of session file.') 
    print('                                 ver_string can be "5.1", "5.2", "6.0" and etc.')
    print('                                 If not specified, the latest version will be used.')
    print('')
    print('    [-user user_string]:         Specify username. This parameter will be used if version > 5.2.')
    print('                                 If not specified, the current username will be used.')
    print('')
    print('    [-sid sid_string]:           Specify SID. This parameter will be used if version >= 5.1.')
    print('                                 If not specified, the current user\'s SID will be used.')
    print('')
    print('    [-key key_string]:           Specify user\'s master password.')
    print('                                 If specified, implicit "-ver 6.0"')
    print('')
    print('    <password_str|base64_str>:   Plain password text or base64-encoded encrypted text.')
    print('')

def main():
    if (len(sys.argv) < 3):
        help()
        return
    
    if sys.argv[1].lower() == '-e':
        bEncrypt = True
    elif sys.argv[1].lower() == '-d':
        bEncrypt = False
    else:
        help()
        return
    
    ver = None
    user = None
    sid = None
    key = None
    targets = []

    i = 2
    while i < len(sys.argv):
        if sys.argv[i].lower() == '-ver':
            if ver != None:
                raise ValueError('Duplicate arguments are found: -ver')
            ver = sys.argv[i + 1]
            i += 1
        elif sys.argv[i].lower() == '-user':
            if user != None:
                raise ValueError('Duplicate arguments are found: -user')
            user = sys.argv[i + 1]
            i += 1
        elif sys.argv[i].lower() == '-sid':
            if sid != None:
                raise ValueError('Duplicate arguments are found: -sid')
            sid = sys.argv[i + 1]
            i += 1
        elif sys.argv[i].lower() == '-key':
            if key != None:
                raise ValueError('Duplicate arguments are found: -key')
            key = sys.argv[i + 1]
            i += 1
        else:
            for j in range(i, len(sys.argv)):
                targets.append(sys.argv[j])
            i += len(targets)
        i += 1

    if ver == None:
        ver = 0xffff
    if key != None:
        ver = 6.0
    
    if key == None and float(ver) >= 5.1 and sid == None:
        sid = GetCurrentSID()
    if key == None and float(ver) > 5.2 and user == None:
        user = GetCurrentUserName()
    
    cipher = XFtpCrypto(SessionFileVersion = ver, 
                        UserName = user, 
                        SID = sid, 
                        MasterPassword = key)
    for target in targets:
        if bEncrypt:
            print(cipher.EncryptString(target))
        else:
            print(cipher.DecryptString(target))

if __name__ == '__main__':
    main()
else:
    print('Please run as script directly.')
