# How Does Xmanager Encrypt password?

## 1. What is Xmanager?
  Xmanager is the market's leading PC X server that brings the power of X applications to a Windows environment.

  With Xmanager, X applications installed on remote UNIX based machines run seamlessly with Windows application side by side.

  It provides a powerful session management console, easy-to-use X application launcher, X server profile management tool, SSH module and a high performance PC X server for securely accessing a remote and virtualized UNIX and Linux environment.

  You can find its official website [here](https://www.netsarang.com/).

## 2. What does indicate that Xmanager encrypts password?
  * If you open Xshell or Xftp in Xmanager and then create a new session, you will find a window like these below:

    <img src = "Xshell_New_Session.png" width = "59%">
    <img src = "Xftp_New_Session.png" width = "40%">


  * After you input your username and password then click "Ok", Xshell and Xftp will save your configuration at

    > __%userprofile%\\Documents\\NetSarang\\Xshell\\Sessions__

    or

    > __%userprofile%\\Documents\\NetSarang\\Xftp\\Sessions__

    Here below is an sample configuration file created by Xftp:

    <img src = "Xftp_config_file.png">

  * You can find there is a field named "Password" in configuration file and the content of this field seems to be encoded by Base64 (Yes, you are right).

## 3. How does Xmanager encrypt password?
  * After disassembling Xmanager by IDA, I find Xmanager use a stream cipher to encrypt password. The stream cipher is an RC4 stream cipher. Here below is what Xmanager did:

    __1. Generate key used in RC4 stream cipher.__  
      * Xmanager use SHA-256 hash algorithm to generate key.

        The key is the SHA-256 digest of the current OS account's SID string.

        You can use `whoami /user` in Command Prompt to check your current OS account's SID string.

        For example if your current OS account's SID string is `S-1-5-21-917267712-1342860078-1792151419-512`, the 32-bytes-long SHA-256 digest is

        ```cpp
        unsigned char Key[32] = {
            0xCE, 0x97, 0xBE, 0xA9, 0x0C, 0x2A, 0x40, 0xB9,
            0x5C, 0xC0, 0x79, 0x74, 0x1D, 0xDC, 0x03, 0xCB,
            0x39, 0xAB, 0x3D, 0xE5, 0x26, 0x7A, 0x3B, 0x11,
            0x05, 0x4B, 0x96, 0x3C, 0x93, 0x6F, 0x9C, 0xD4
        };
        ```

      * __NOTICE:__  
        Start from __Xmanager Enterprise 5 (Build 1249)__: (Maybe lower)

        > Xshell.exe: 5.0.0052,  
        > Xftp.exe: 5.0.0051,  
        > nssock2.dll: 5.0.0028,  
        > nsssh3.dll: 5.0.0045,  
        > nsprofile2.dll: 5.0.0028,  
        > nslicense.dll: 5.0.0026,  
        > nsutil2.dll: 5.0.0037,  
        > nsverchk.exe: 5.0.0011,  
        > Xagent.exe: 5.0.0020  

        Xmanager Changes the algorithm of generating key. Now the key is the SHA-256 digest of the combination of current OS account's name(case sensitive) and current OS account's SID string.

        For example if your current OS account's name is `Administrator` and current OS account's SID string is `S-1-5-21-917267712-1342860078-1792151419-512`, the key is the 32-bytes-long SHA-256 digest of `AdministratorS-1-5-21-917267712-1342860078-1792151419-512`, exactly speaking:

        ```cpp
        unsigned char Key[32] = {
            0x8E, 0x12, 0x29, 0xDC, 0x1F, 0x34, 0x56, 0xB9,
            0xBB, 0xCD, 0x94, 0xC2, 0xAB, 0x0A, 0xF3, 0xB9,
            0x95, 0x96, 0x6F, 0x06, 0xE3, 0x9D, 0x24, 0x80,
            0x6A, 0x74, 0xCD, 0x7E, 0x0B, 0x69, 0xB3, 0x78
        };
        ```

    __2. Calculate SHA-256 digest of original password.__
      * if your original password is "This is a test", the SHA-256 digest is:

        ```cpp
        unsigned char CheckCode[32] = {
            0xC7, 0xBE, 0x1E, 0xD9, 0x02, 0xFB, 0x8D, 0xD4,
            0xD4, 0x89, 0x97, 0xC6, 0x45, 0x2F, 0x5D, 0x7E,
            0x50, 0x9F, 0xBC, 0xDB, 0xE2, 0x80, 0x8B, 0x16,
            0xBC, 0xF4, 0xED, 0xCE, 0x4C, 0x07, 0xD1, 0x4E
        };
        ```

        The 32-bytes-long data will be regarded as the checksum appended to the encrypted password.

    __3. Initialize cipher.__
      * Xmanager use the key generated to initialize RC4 cipher.

    __4. Encrypt password.__
      * Xmanager use the initialized RC4 cipher encrypt original password.

        If the original password is "This is a test", the result is

        ```cpp
        unsigned char encrypted_pwd[] = {
            0x84, 0x83, 0x31, 0x23, 0x24, 0x37, 0x1D, 0xB2,
            0x6C, 0x54, 0x87, 0x5B, 0x6E, 0xE9
        };
        ```

      * __NOTICE:__  
        After __Xmanager Enterprise 5 (Build 1249)__: (Maybe lower)

        the result should be

        ```cpp
        unsigned char encrypted_pwd[] = {
            0xCE, 0xFD, 0xB5, 0x3B, 0x5C, 0x78, 0xDE, 0xA4,
            0x6C, 0xDD, 0xCE, 0x4D, 0x72, 0x40
        };
        ```

    __5. Append checksum to encrypted password.__
      * The final result is the encrypted password with the checksum.

        __EXAMPLE:__
        ```cpp
        unsigned char final_result[] = {
            0x84, 0x83, 0x31, 0x23, 0x24, 0x37, 0x1D, 0xB2,
            0x6C, 0x54, 0x87, 0x5B, 0x6E, 0xE9, 0xC7, 0xBE,
            0x1E, 0xD9, 0x02, 0xFB, 0x8D, 0xD4, 0xD4, 0x89,
            0x97, 0xC6, 0x45, 0x2F, 0x5D, 0x7E, 0x50, 0x9F,
            0xBC, 0xDB, 0xE2, 0x80, 0x8B, 0x16, 0xBC, 0xF4,
            0xED, 0xCE, 0x4C, 0x07, 0xD1, 0x4E
        };
        ```

      * __NOTICE:__  
        After __Xmanager Enterprise 5 (Build 1249)__: (Maybe lower)

        the result should be

        ```cpp
        unsigned char encrypted_pwd[] = {
            0xCE, 0xFD, 0xB5, 0x3B, 0x5C, 0x78, 0xDE, 0xA4,
            0x6C, 0xDD, 0xCE, 0x4D, 0x72, 0x40, 0xC7, 0xBE,
            0x1E, 0xD9, 0x02, 0xFB, 0x8D, 0xD4, 0xD4, 0x89,
            0x97, 0xC6, 0x45, 0x2F, 0x5D, 0x7E, 0x50, 0x9F,
            0xBC, 0xDB, 0xE2, 0x80, 0x8B, 0x16, 0xBC, 0xF4,
            0xED, 0xCE, 0x4C, 0x07, 0xD1, 0x4E
        };
        ```

    __6. Convert the final result to Base64 format and store it in configuration file.__
      * Convert the final result to Base64 format. Then store it to configuration file.

        __EXAMPLE__: `hIMxIyQ3HbJsVIdbbunHvh7ZAvuN1NSJl8ZFL11+UJ+82+KAixa89O3OTAfRTg==`  

      * __NOTICE:__  
        After __Xmanager Enterprise 5 (Build 1249)__: (Maybe lower)  
        it should be `zv21O1x43qRs3c5NckDHvh7ZAvuN1NSJl8ZFL11+UJ+82+KAixa89O3OTAfRTg==`

## 4. How to use XmanagerCrypto.py
  * Make sure that you have installed `Python3`.
  * Make sure that you have installed `pypiwin32`, `pycryptodome` module.

  1. __Encrypt Password:__

     ```cmd
     E:\GitHub\how-does-Xmanager-encrypt-password\python3\Xmanager5CryptoHelper.py -e "This is a test"
     zv21O1x43qRs3c5NckDHvh7ZAvuN1NSJl8ZFL11+UJ+82+KAixa89O3OTAfRTg==

     ```

  2. __Decrypt Password:__

     ```cmd
     E:\GitHub\how-does-Xmanager-encrypt-password\python3\Xmanager5CryptoHelper.py -d "zv21O1x43qRs3c5NckDHvh7ZAvuN1NSJl8ZFL11+UJ+82+KAixa89O3OTAfRTg=="
     This is a test

     ```
