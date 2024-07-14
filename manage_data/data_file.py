from __future__ import annotations
import atexit
import json 
from base64 import b64encode, b64decode
from exceptions import UnableToDecodeTheFile

from aes_encryption import AES_Encripton



class Data(dict):
    def __init__(self):
        super().__init__()
        self["Internet"] = []
        self["Emails"] = []
        self["Crypto"] = []
        self["Development"] = []
        self["Databases"] = []
        self["Funds"] = []
        self["Payments"] = []
        self["Apps"] = []
        

class IODataFile:
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path
        
    def get_data(self) -> str:
        with open(self._file_path, "r", encoding="utf-8") as f:
            data = f.read()
        return data
        
    def save_data(self, data: str) -> None:
        with open(self._file_path, "w", encoding="utf-8") as f:
            f.write(data)


class DataFile:
    def __init__(self, file_path: str) -> None:
        self._io = IODataFile(file_path)
        self._aes_encryption = AES_Encripton()
        
        self._password: str
        self._data: Data 
        
        # print(f'{self._password = }')
        
        # atexit.register(self.backup)
    
    # def backup(self):
    #     ...
    
    def create_new_data_file(self) -> None:
        self._data = Data()
        self.save_data()
    
    def load_data(self) -> Data:
        b64_string = self._io.get_data()
        encrypted_bytes_data = b64decode(b64_string) 
        try:
            decrypted_bytes_data = self._aes_encryption.decrypt(self._password, encrypted_bytes_data)
        except ValueError:
            raise ValueError('Unable to decrypt')
        decrypted_json_data = decrypted_bytes_data.decode('utf-8')
        self._data = json.loads(decrypted_json_data)
        return self._data
    
    def save_data(self) -> None:
        json_data = json.dumps(self._data)
        bytes_data = json_data.encode('utf-8')
        encrypted_bytes_data = self._aes_encryption.encrypt(self._password, bytes_data)
        b64_encrypted_data = b64encode(encrypted_bytes_data).decode('utf-8')
        self._io.save_data(b64_encrypted_data)
        
    @property
    def get_data(self) -> Data:
        return self._data

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, pswd: str):
        self._password = pswd 
     
                
d = DataFile('./testfile')
d.password = 'hello'

# d.create_new_data_file()

r = d.load_data()

print(r)
