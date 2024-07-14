import copy 

class Entry:
    def __init__(self):
        self._data = ["New Record", "Username", 'password11', "URL", "N/A"]
    
    @property
    def data(self):
        return self._data
    
    def __str__(self):
        return f'{self._data}'