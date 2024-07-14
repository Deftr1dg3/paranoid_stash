from __future__ import annotations
import atexit
import json 
import copy
from base64 import b64encode, b64decode
from exceptions import UnableToDecodeTheFile
from typing import NamedTuple

from aes_encryption import AES_Encripton
from entry import Entry


class Data(dict):
    _default_categories = ["Internet", "Emails", "Crypto", "Development", "Databases", "Funds", "Payments", "Apps"]
    def __init__(self, data: list[list] | None = None):
        super().__init__()
        if data is None:
            for category in self._default_categories:
                self[category] = list()
        else:
            for key, value in data:
                self[key] = value
                

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
    def data(self) -> Data:
        return self._data
    
    @data.setter
    def data(self, new_data: Data) -> None:
        self._data = new_data 

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, pswd: str):
        self._password = pswd 
     

class State(NamedTuple):
    data: Data 
    selected_category: str | None
    selcted_entity: int | None

  
class DataState:
    _data_state = []
    
    def __init__(self):
        self._current_index = -1
    
    def add(self, data_state: ManageData) -> None:
        state = copy.deepcopy(data_state)
        data = state.data 
        selected_category = state.selected_category
        selected_entity = state.selected_entity
        
        self._current_index += 1
        self._data_state.insert(self._current_index, State(data=data, selected_category=selected_category, selcted_entity=selected_entity))
        self._data_state = self._data_state[:self._current_index + 1]

    def forward(self) -> State:
        if self._current_index < len(self._data_state):
            self._current_index += 1 
        return self._data_state[self._current_index]
    
    def backward(self) -> State:
        if self._current_index > 0:
            self._current_index -= 1
        return self._data_state[self._current_index]
    


class ManageData:

    _default_entity = ["New Record", "Username", 'password11', "URL", "N/A"]
    
    def __init__(self, df: DataFile) -> None:
        self._df = df 
        self._data = df.load_data()
        self._state = DataState()
        
        self.selected_category: str | None = None
        self.selected_entity: int | None = None
        
        self._state.add(self)
    
    @property
    def data(self):
        return self._data
    
    def _get_category_index(self, category: str) -> int:
        items = self._data.keys()
        i = 0
        for itm in items:
            if itm == category:
                return i 
            i += 1
        raise ValueError('The category is not defined.')

    def _get_entity_index(self, category: str, entity: list) -> int:
        entities = self._data.get(category, None)
        if entities is None:
            raise ValueError(f'The category "{category}" is not defined.')
        for i in range(len(entities)):
            if entities[i] == entity:
                return i 
        raise ValueError('Provided entity is not under the category')
    
    # Categories ------------------------------------------------------------------------
    
    def add_category(self, category: str) -> None:
        if category in self._data:
            raise KeyError(f'Category with such name => {category} already in data.')
        self._data[category] = list()
        self._df.save_data() 
        self._state.add(self)
    
    def get_categories(self) -> list:
        return list(self._data.keys())
    
    def get_category_data(self, category: str) -> list:
        if category not in self._data:
            raise KeyError(f'Category "{category}" is not in the data file.')
        return self._data[category]
    
    def rename_category(self, new_category: str) -> None:
        if not self.selected_category:
            raise KeyError('No category selected.')
        
        items = [list(row) for row in self._data.items()]
        category_index = self._get_category_index(self.selected_category)
        items[category_index][0] = new_category
        new_data = Data(items)
        
        self._data = new_data
        self._df.data = self._data
        self._df.save_data()
        self._state.add(self)
            
    def move_category(self, category: str, direction: int = 1) -> None:
        if category not in self._data:
            raise KeyError(f'Category "{category}" is not in the data file.')
        
        step = 1
        step *= direction
        items = [list(row) for row in self._data.items()]
        category_index = self._get_category_index(category)
        
        try:
            items[category_index], items[category_index - step] = items[category_index - step], items[category_index]
        except IndexError:
            raise IndexError('Unable to continue moving in this direction.')
        else:
            new_data = Data(items)
            self._data = new_data 
            self._df.data = self._data 
            self._df.save_data()
            self._state.add(self)
            
    def clear_category(self, category: str) -> None:
        if category not in self._data:
            raise KeyError(f'Category "{category}" is not in the data file.')
        self._data[category].clear()
        self._df.save_data()
        self._state.add(self)
          
    def delete_category(self, category: str) -> None:
        if category not in self._data:
            raise KeyError(f'Category "{category}" is not in the data file.')
        del self._data[category]
        self._df.save_data()
        self._state.add(self)
        
    # Entities ------------------------------------------------------------------------
        
    def add_entity(self, category: str) -> None:
        if category not in self._data:
            raise KeyError(f'Category "{category}" is not in the data file.')
        
        new_entity = copy.deepcopy(self._default_entity)
        self.selected_entity = id(new_entity)
        
        self._data[category].append(new_entity)
        self._df.save_data()
        self._state.add(self)
    
    def move_entity(self, category: str, entity_ind: int, up: bool = True) -> None:
        if category not in self._data:
            raise KeyError(f'Category "{category}" is not in the data file.')
    
    def delete_entity(self, category: str, entity_ind: int) -> None:
        if category not in self._data:
            raise KeyError(f'Category "{category}" is not in the data file.')
    
    def adjust_entity(self, category: str, entity_ind: int) -> None:
        if category not in self._data:
            raise KeyError(f'Category "{category}" is not in the data file.')
        
    # Manage instance states ------------------------------------------------------------------------
    
    def forward(self):
        next_state = self._state.forward()
        
        self._data = next_state.data
        self.selected_category = next_state.selected_category
        self.selected_entity = next_state.selcted_entity
        
        self._df.data = self._data
        self._df.save_data()
    
    def backward(self):
        prev_state = self._state.backward()
        
        self._data = prev_state.data
        self.selected_category = prev_state.selected_category
        self.selected_entity = prev_state.selcted_entity
        
        self._df.data = self._data
        self._df.save_data()
         
    def __str__(self):
        return f'{self._data}'




                
d = DataFile('./testfile')
d.password = 'hello'

# d.create_new_data_file()

md = ManageData(d)

print(md)

md.selected_category = 'Emails'


md.clear_category(md.selected_category)

md.add_entity(md.selected_category)
print(md)
print()

md.add_entity(md.selected_category)
print(md)
print()

# md.clear_category(md.selected_category)
# print(md)
# print()

# md.backward()
# print(md)
# print()

# md.backward()
# print(md)
# print()

# md.backward()
# print(md)
# print()

# md.forward()
# print(md)
# print()



# md.move_category(md.selected_category)
# print(md)

# md.move_category(md.selected_category)
# print(md)

# md.move_category(md.selected_category)
# print(md)

# md.move_category(md.selected_category)
# print(md)
