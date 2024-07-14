#!/usr/bin/env python3


import os
from hashlib import pbkdf2_hmac
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


# AES key can be either 16, 24, or 32 bytes long.
# AES block size is always 16 bytes.


class AES_Encripton:
	
    def __init__(self) -> None:
        self._key_iterations_count = 100_000
        self._salt_size = AES.block_size
        
    def _get_salt(self) -> bytes:
        salt = os.urandom(self._salt_size)
        return salt
         
    def _get_key(self, password: str, salt: bytes) -> bytes:
        key = pbkdf2_hmac("sha256", password.encode("utf-8"), salt, self._key_iterations_count)
        return key

    def encrypt(self, password: str, bytes_data: bytes) -> bytes:
        salt = self._get_salt()
        encryption_key = self._get_key(password, salt)
        padded_bytes_data = pad(bytes_data, AES.block_size) 
        
        cipher = AES.new(encryption_key, AES.MODE_CBC)
        encrypted_bytes_data = cipher.encrypt(padded_bytes_data)
        encrypted_bytes_packet = bytes(cipher.iv) + salt + encrypted_bytes_data  
        
        return encrypted_bytes_packet

    def decrypt(self, password: str, encrypted_bytes_data: bytes) -> bytes:
        iv = encrypted_bytes_data[:AES.block_size]
        salt = encrypted_bytes_data[AES.block_size: AES.block_size + self._salt_size]
        encrypted_bytes_data = encrypted_bytes_data[self._salt_size + AES.block_size:]
        
        decryption_key = self._get_key(password, salt) 
        cipher = AES.new(decryption_key, AES.MODE_CBC, iv=iv)
        
        padded_decrypted_bytes_data = cipher.decrypt(encrypted_bytes_data)
        decrypted_bytes_data = unpad(padded_decrypted_bytes_data, AES.block_size)
        
        return decrypted_bytes_data
    
    
   
# def main():
#     aes = AES_Encripton() 
    
#     plain_text = 'Some text here'
#     p = 'password'
#     en = aes.encrypt(p, plain_text.encode('utf-8'))
#     print(en)
#     p = 'password'
#     en = os.urandom(32)
#     print(f'{en = }')
#     dec = aes.decrypt(p, en)
    
#     print(dec.decode('utf-8'))
    
# if __name__ == '__main__':
#     main()