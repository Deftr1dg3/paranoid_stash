from __future__ import annotations
import atexit
import json 
import copy
from base64 import b64encode, b64decode
from typing import NamedTuple

from .aes_encryption import AES_Encripton
from .manage_password import GeneratePassword, PasswordStrength


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
    def __init__(self, settings: dict) -> None:
        self._io = IODataFile(settings['data_file'])
        self._aes_encryption = AES_Encripton()
        
        self._password: str
        self._data: Data 
        
        # print(f'{self._password = }')
        
        # atexit.register(self.backup)
    
    # def backup(self):
    #     ...
    
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
     

class State(NamedTuple):
    data: Data 
    selected_category: str | None
    selected_entry: int | None

  
class DataState:
    _data_state = []
    
    def __init__(self):
        self._current_index = -1
    
    def add(self, data_state: ManageData) -> None:
        state = copy.deepcopy(data_state)
        data = state.data 
        selected_category = state.selected_category
        selected_entry = state.selected_entry
        
        self._current_index += 1
        self._data_state.insert(self._current_index, State(data=data, selected_category=selected_category, selected_entry=selected_entry))
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

    _default_entry = ["New Record", "Username", 'password111', "URL", "N/A"]
    
    def __init__(self, df: DataFile) -> None:
        self._df = df 
        self._data = df.data
        self._state = DataState()
        self._pass_gen = GeneratePassword()
        
        self.search_results: list | None = None
        self.selected_category: str | None = None
        self.selected_entry: int | None = None
        
        self.save_state()
    
    @property
    def data(self):
        return self._data
    
    def get_category_index(self, category: str) -> int:
        items = self._data.keys()
        i = 0
        for itm in items:
            if itm == category:
                return i 
            i += 1
        return -1

    def get_entry_index(self, entry_id: int) -> tuple[str, int]:
        for category in self._data.keys():
            for i in range(len(self._data[category])):
                if id(self._data[category][i]) == entry_id:
                    return category, i
        return ('', -1)

    def update(self) -> None:
        self._df.save_data()
        
    def save_state(self):
        self._state.add(self)
    
    # Categories ------------------------------------------------------------------------
    
    def add_category(self, category: str) -> None:
        if category in self._data:
            raise KeyError(f'Category with such name => {category} already in data.')
        self._data[category] = list()
        self.selected_category = category
        self.update() 
        self.save_state()
    
    def all_categories(self) -> list:
        return list(self._data.keys())
    
    def get_category_data(self, category: str) -> list:
        if category not in self._data:
            return []
        return self._data[category]
    
    def rename_category(self, new_category: str) -> None:
        if not self.selected_category:
            raise KeyError('No category selected.')
        
        items = [list(row) for row in self._data.items()]
        category_index = self.get_category_index(self.selected_category)
        items[category_index][0] = new_category
        new_data = Data(items)
        
        self._data = new_data
        self._df.data = self._data
        self.update()
        self.save_state()
            
    def move_category(self, direction: int = -1) -> None:
        if self.selected_category is None:
            return

        items = [list(row) for row in self._data.items()]
        category_index = self.get_category_index(self.selected_category)
        
        step = 1 * direction 
        swap = category_index + step 
        if 0 <= swap < len(items):
            items[category_index], items[swap] = items[swap], items[category_index]
            new_data = Data(items)
            
            self._data = new_data 
            self._df.data = self._data 
            self.update()
            self.save_state()
            
    def clear_category(self) -> None:
        if self.selected_category is None:
            return 
        self._data[self.selected_category].clear()
        self.update()
        self.save_state()
          
    def delete_category(self) -> None:
        if self.selected_category is None:
            return 
        del self._data[self.selected_category]
        self.update()
        self.save_state()
        
    # Entities ------------------------------------------------------------------------
        
    def add_entry(self) -> bool:
        if self.selected_category is not None:
            new_entry = copy.deepcopy(self._default_entry)
            password_strength = PasswordStrength()
            new_entry[2] = self._pass_gen.generate_password(password_strength.STRONG)
            self.selected_entry = id(new_entry)
            self._data[self.selected_category].append(new_entry)
            self.update()
            self.save_state()
            return True 
        return False
    
    def move_entry(self, direction: int = -1) -> None:
        if self.selected_entry is None:
            return
        category, e_ind = self.get_entry_index(self.selected_entry)
        if not e_ind == -1:
            step = 1 * direction 
            swap = e_ind + step
            if 0 <= swap < len(self._data[category]) and self.selected_category == category:
                self._data[category][e_ind], self._data[category][swap] = self._data[category][swap], self._data[category][e_ind]
                self.update()
                self.save_state()
    
    def get_entry_by_id(self, entry_id: int) -> list | None:
        category, e_ind = self.get_entry_index(entry_id)
        if not e_ind == -1:
            return self._data[category][e_ind]
    
    def get_selected_entry(self) -> list | None:
        if self.selected_entry is None:
            return 
        return self.get_entry_by_id(self.selected_entry)
        
    def delete_entry(self) -> None:
        if self.selected_entry is None:
            return
        category, e_ind = self.get_entry_index(self.selected_entry)
        if not e_ind == -1:
            del self._data[category][e_ind]
            self.update()
            self.save_state()
    
    # Search ------------------------------------------------------------------------

    def search(self, pattern: str) -> list[list] | None:
        results = []
        if not pattern:
            self.search_results = None 
            return
        for category in self._data.keys():
            for entry in self._data[category]:
                if pattern.lower() in entry[0].lower():
                    results.append(entry)
        self.search_results = results
        return results

        
    # Manage instance states ------------------------------------------------------------------------
    
    def forward(self):
        next_state = self._state.forward()
        
        self._data = next_state.data
        self.selected_category = next_state.selected_category
        self.selected_entry = next_state.selected_entry
        
        self._df.data = self._data
        self.update()
    
    def backward(self):
        prev_state = self._state.backward()
        
        self._data = prev_state.data
        self.selected_category = prev_state.selected_category
        self.selected_entry = prev_state.selected_entry
        
        self._df.data = self._data
        self.update()
         
    def __str__(self):
        return f'{self._data}'



# Tests ------------------------------------------------------------------------


# SETTINGS_PATH = './settings.json'
# with open(SETTINGS_PATH, 'r') as f:
#     settings = json.load(f)
                
# d = DataFile(settings)
# d.password = 'hello'

# # d.create_new_data_file()

# md = ManageData(d)

# print(md)
# print()


# md.selected_category = 'Apps'


# md.clear_category(md.selected_category)

# print(md)
# print()

# md.delete_category('New Name Fro Crypto')

# print(md)
# print()

# md.add_entity()
# print(md)
# print()

# md.add_entity()
# print(md)
# print()

# md.clear_category(md.selected_category)
# print(md)
# print()

# md.backward()
# print(md)
# print()

# md.forward()
# print(md)
# print()

# ent_id = id(md._data[md.selected_category][0])

# print(f"{ent_id = } {md.get_entity_by_id(ent_id) = }\nDeleting ... \n")

# md.delete_entity(ent_id)
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
