
import os 
import wx
import json
from pathlib import Path

from GUI.main_frame import MainFrame 
from GUI.modals.first_launch import FirstLaunchFrame
from GUI.modals.get_password_from_user import GetPasswordFrame
from manage_data import ManageData, DataFile

class GUIApp(wx.App):
    def __init__(self, settings: dict):
        super().__init__()
        self._general_settings = settings 
        self._gui_settings = self._get_data_from_file(Path(self._general_settings['gui_settings']))
        self._color_themes = self._get_data_from_file(Path(self._general_settings['color_themes']))
        self._current_theme = self._general_settings['color_theme']
        
        self._data_file = DataFile(self._general_settings['data'])
        self._data_file_path = Path(self._general_settings['data']['data_file'])
        
        if not self._data_file_path.exists():
            self.first_launch()
        else:
            self.get_password()


    def get_password(self):
        self._get_password = GetPasswordFrame(self._data_file, self._gui_settings, self._color_themes, self._current_theme, self)
        self._get_password.Show()
        
    
    def first_launch(self):
        self._first_launch = FirstLaunchFrame(self._data_file, self._gui_settings, self._color_themes, self._current_theme, self)
        self._first_launch.Show()
            
    
    def _get_data_from_file(self, file_path: Path) -> dict:
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} was not found.")
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    
        
    def LaunchMainApp(self):
        
        self._manage_data = ManageData(self._data_file)
        self._main_frame = MainFrame(self._manage_data, self._gui_settings, self._color_themes, self._current_theme)
        self._main_frame.Show()