from __future__ import annotations
import atexit
import json 
import copy
from base64 import b64encode, b64decode
from typing import NamedTuple

from .aes_encryption import AES_Encripton
from .manage_password import GeneratePassword, PasswordStrength
from manage_data.backup.backup import BackUp

from pathlib import Path

# SETTINGS = "settings.json"

import logging 

log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(
    filename='app.log', 
    level=logging.DEBUG, 
    format=log_format
)

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
    def __init__(self, settings: dict) -> None:
        self._settings = settings 
        self._file_path = Path(self._settings['data_file'])
        self._settings_path = Path(self._settings['settings_path'])
    
    @property
    def file_path(self) -> Path:
        return self._file_path 
    
    @file_path.setter
    def file_path(self, path: str) -> None:
        new_path = Path(path).with_suffix(self._settings['extension'])
        self._settings['data_file'] = str(new_path)
        self.save_new_datafile_path(str(new_path))
        self._file_path = new_path
    
    def save_new_datafile_path(self, path: str):
        with open(self._settings_path, 'r') as f:
            data = json.load(f)
        data['data'].update(self._settings)
        with open(self._settings_path, 'w') as f:
            json.dump(data, f, indent=2)
        
    def get_data(self, path: Path | None = None) -> str:
        if path is None:
            path = self._file_path
        with open(path, "r", encoding=self._settings['encoding']) as f:
            data = f.read()
        return data
        
    def save_data(self, data: str, path: Path | None = None) -> None:
        if path is None:
            path = self._file_path
        with open(path, "w", encoding=self._settings['encoding']) as f:
            f.write(data)


class DataFile:
    def __init__(self, settings: dict) -> None:
        self._settings = settings 
        
        self.io = IODataFile(settings)
        self._aes_encryption = AES_Encripton()
        self._backup = BackUp(settings)
        
        self._json_data: str
        self._b64_encrypted_data: str
        self._data: Data 
        
        self._password: str = ""
        self._password_backup: str = ""
        
        atexit.register(self.backup)
        
    
    def backup(self) -> str | None:
        if self.save_data():
            created = self._backup.save_backup_file(json_data=self._json_data, b64_data=self._b64_encrypted_data)
            return created
    
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
        self.change_datafile_path(self._settings['default_datafile_path'])
        self.save_data()
    
    def load_data(self, path: str | None = None) -> Data:
        if path is not None:
            target_path = Path(path)
        else:
            target_path = None
            
        b64_string = self.io.get_data(target_path)
        encrypted_bytes_data = b64decode(b64_string) 
        try:
            decrypted_bytes_data = self._aes_encryption.decrypt(self._password, encrypted_bytes_data)
        except ValueError:
            raise ValueError('Unable to decrypt')
        decrypted_json_data = decrypted_bytes_data.decode(self._settings['encoding'])
        self._data = json.loads(decrypted_json_data)
        return self._data
    
    def save_data(self) -> bool:
        try:
            self._json_data = json.dumps(self._data)
        except AttributeError:
            return False
        bytes_data = self._json_data.encode(self._settings['encoding'])
        encrypted_bytes_data = self._aes_encryption.encrypt(self._password, bytes_data)
        self._b64_encrypted_data = b64encode(encrypted_bytes_data).decode(self._settings['encoding'])
        self.io.save_data(self._b64_encrypted_data)
        return True
    
    def change_datafile_path(self, new_path: str):
        self.io.file_path = new_path
    
    def restore_default_datafile_path(self):
        self.io.file_path = self._settings['default_datafile_path']
    
    def backup_password(self):
        self._password_backup = self._password
    
    def restore_password(self):
        self._password = self._password_backup
     

class State(NamedTuple):
    data: Data 
    selected_category: str | None
    selected_entry_ind: int | None
    search_results: list | None

  
class DataState:
    
    def __init__(self):
        self._undo = []
        self._redo = []
        self._max_stack_len = 1000
    
    def add(self, data_state: ManageData) -> None:
            
        if data_state.selected_entry is not None:
            selected_entry_ind = data_state.get_entry_index(data_state.selected_entry)
        else:
            selected_entry_ind = -1
        
        state = copy.deepcopy(data_state) 
        data = state.data 
        selected_category = state.selected_category
        search_results = state.search_results
        
        new_state = State(data=data,
                            selected_category=selected_category,
                            selected_entry_ind=selected_entry_ind,
                            search_results=search_results)
        
        self._undo.append(new_state)

    def forward(self) -> State | None:
        if self._redo:
            state = self._redo.pop()
            self._undo.append(state)
            return state 
        return None
    
    def backward(self) -> State | None:
        if self._undo:
            if len(self._undo) > 1:
                state = self._undo.pop()
                self._redo.append(state)
            else:
                state = self._undo[0]
            return state 
        return None
    

class ManageData:

    _default_entry = ["New Record", "Username", 'password111', "URL", "N/A"]
    
    def __init__(self, df: DataFile) -> None:
        self._df = df 
        # self._df.data = df.data
        self._state = DataState()
        self._pass_gen = GeneratePassword()
        
        self.search_results: list | None = None
        self.selected_category: str | None = None
        self.selected_entry: int | None = None
        
        self.save_state()
    
    @property
    def data(self) -> Data:
        return self._df.data
    
    @data.setter
    def data(self, new_data: Data):
        self._df.data = new_data
    
    def get_category_index(self, category: str) -> int:
        items = self._df.data.keys()
        i = 0
        for itm in items:
            if itm == category:
                return i 
            i += 1
        return -1

    def get_entry_index(self, entry_id: int) -> int:
        if self.selected_category is not None:
            category_content = self._df.data[self.selected_category]
            for i in range(len(category_content)):
                if id(category_content[i]) == entry_id:
                    return i
                    
        if self.search_results is not None:       
            for i in range(len(self.search_results)):
                if id(self.search_results[i]) == self.selected_entry:
                    return i       
        return -1
    
    def get_entry_category_and_index(self, entry_id: int) -> tuple[str, int]:
        for category in self.all_categories():
            for i in range(len(self._df.data[category])):
                if id(self._df.data[category][i]) == entry_id:
                    return category, i 
        return "", -1

    def update(self) -> None:
        self._df.save_data()
        
    def save_state(self):
        self._state.add(self)
    
    # Categories ------------------------------------------------------------------------
    
    def add_category(self, category: str) -> None:
        if category in self._df.data:
            raise KeyError(f'Category with such name => {category} already in data.')
        self._df.data[category] = list()
        self.selected_category = category
        self.update() 
        self.save_state()
    
    def all_categories(self) -> list:
        return list(self._df.data.keys())
    
    def get_category_data(self, category: str) -> list:
        if category not in self._df.data:
            return []
        return self._df.data[category]
    
    def rename_category(self, new_category: str) -> None:
        if self.selected_category is None:
            return 
        items = [list(row) for row in self._df.data.items()]
        category_index = self.get_category_index(self.selected_category)
        items[category_index][0] = new_category
        new_data = Data(items)
        
        self._df.data = new_data
        self._df.data = self._df.data
        self.selected_category = new_category
        self.update()
        self.save_state()
            
    def move_category(self, direction: int = -1) -> None:
        if self.selected_category is None:
            return

        items = [list(row) for row in self._df.data.items()]
        category_index = self.get_category_index(self.selected_category)
        
        step = 1 * direction 
        swap = category_index + step 
        if 0 <= swap < len(items):
            items[category_index], items[swap] = items[swap], items[category_index]
            new_data = Data(items)
            
            self._df.data = new_data 
            self._df.data = self._df.data 
            self.update()
            self.save_state()
            
    def clear_category(self) -> None:
        if self.selected_category is None:
            return 
        self._df.data[self.selected_category].clear()
        self.update()
        self.save_state()
          
    def delete_category(self) -> None:
        if self.selected_category is None:
            return 
        del self._df.data[self.selected_category]
        self.selected_category = None
        self.selected_entry = None
        self.update()
        self.save_state()
        
    # Entities ------------------------------------------------------------------------
        
    def add_entry(self) -> bool:
        if self.selected_category is not None:
            new_entry = copy.deepcopy(self._default_entry)
            password_strength = PasswordStrength()
            new_entry[2] = self._pass_gen.generate_password(password_strength.STRONG)
            self.selected_entry = id(new_entry)
            self._df.data[self.selected_category].append(new_entry)
            self.update()
            self.save_state()
            return True 
        return False
    
    def move_entry(self, direction: int = -1) -> None:
        if self.selected_entry is None:
            return
        if self.search_results is not None:
            return
        e_ind = self.get_entry_index(self.selected_entry)
        if not e_ind == -1:
            step = 1 * direction 
            swap = e_ind + step
            if 0 <= swap < len(self._df.data[self.selected_category]):
                self._df.data[self.selected_category][e_ind], self._df.data[self.selected_category][swap] = self._df.data[self.selected_category][swap], self._df.data[self.selected_category][e_ind]
                self.update()
                self.save_state()
    
    def get_entry_by_id(self, entry_id: int) -> list | None:
        e_ind = self.get_entry_index(entry_id)
        if self.search_results is not None:
            return self.search_results[e_ind]
        if not e_ind == -1:
            return self._df.data[self.selected_category][e_ind]
    
    def get_selected_entry(self) -> list | None:
        if self.selected_entry is None:
            return 
        return self.get_entry_by_id(self.selected_entry)
        
    def delete_entry(self) -> None:
        if self.selected_entry is None:
            return
        e_ind = self.get_entry_index(self.selected_entry)
        if not e_ind == -1:
            del self._df.data[self.selected_category][e_ind]
            self.selected_entry = None
            self.update()
            self.save_state()
    
    def move_entry_to_category(self, category: str) -> bool:
        if self.selected_entry is None:
            return False 
        current_category, entry_index = self.get_entry_category_and_index(self.selected_entry)
        if current_category == category:
            return True
        last_index = len(self._df.data[current_category]) - 1
        self._df.data[current_category][entry_index], self._df.data[current_category][last_index] = self._df.data[current_category][last_index], self._df.data[current_category][entry_index]
        entry = self._df.data[current_category].pop()
        self._df.data[category].append(entry)
        self.selected_entry = None
        return True
        
    
    # Search ------------------------------------------------------------------------

    def search(self, pattern: str) -> list[list] | None:
        results = []
        if not pattern:
            self.search_results = None 
            return
        for category in self._df.data.keys():
            for entry in self._df.data[category]:
                if pattern.lower() in entry[0].lower():
                    results.append(entry)
        self.search_results = results
        return results

        
    # Manage instance states ------------------------------------------------------------------------
    
    def get_entry_id_by_index(self, index: int | None) -> int | None:
        if index is None or index == -1:
            return
        if self.selected_category:
            return id(self._df.data[self.selected_category][index])
        if self.search_results:
            return id(self.search_results[index])
    
    
    def forward(self) -> bool:
        next_state = self._state.forward()
        
        # print(f'{len(self._state._undo) = }')
        # print(f'{len(self._state._redo) = }')
        
        if next_state is not None:
            
            self._df.data = next_state.data
            self._df.data = self._df.data
            
            self.selected_category = next_state.selected_category
            self.search_results = next_state.search_results
            
            self.selected_entry = self.get_entry_id_by_index(next_state.selected_entry_ind)
            
            # self.print_attrs()

            self.update()
            return True
        return False
    
    def backward(self) -> bool:
        prev_state = self._state.backward()
        
        # print(f'{len(self._state._undo) = }')
        # print(f'{len(self._state._redo) = }')
        
        if prev_state is not None:
        
            self._df.data = prev_state.data
            self._df.data = self._df.data
            
            self.selected_category = prev_state.selected_category
            self.search_results = prev_state.search_results
            
            self.selected_entry = self.get_entry_id_by_index(prev_state.selected_entry_ind)
            
            # self.print_attrs()
            
            self.update()
            return True 
        return False
         
    # def print_attrs(self):
    #     print(f'{self.selected_category = }')
    #     print(f'{self.selected_entry = }')
        # print(f'{self.search_results = }\n')
    
    # Password ------------------------------------------------------------------------

    def change_password(self, new_password: str):
        ...
        self.update()
        self.save_state()
    
    # Password ------------------------------------------------------------------------

    def __str__(self):
        return f'{self._df.data}'



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
