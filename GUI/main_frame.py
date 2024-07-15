import sys 
import os 
sys.path.append(os.getcwd())

import wx
import json
import ast

from manage_data import ManageData, DataFile
from manage_data import GeneratePassword, ValidatePassword, PasswordStrength

from GUI.main_panel import MainPanel



SETTINGS_PATH = './GUI/gui_settings.json'
COLOR_THEMES_PATH = './GUI/color_themes.json'

with open(SETTINGS_PATH, 'r') as f:
    SETTINGS = json.load(f)

with open(COLOR_THEMES_PATH, 'r') as f:
    COLOR_THEMES: dict = json.load(f)

class MainFrame(wx.Frame):
    def __init__(self, manage_data: ManageData, theme_name: str) -> None:
        super().__init__(None)
        self._manage_data = manage_data
        self._settings = SETTINGS
        self._color_themes = COLOR_THEMES
        self._theme_name = theme_name
        
        size = ast.literal_eval(SETTINGS['mainframe_size']['size'])
        min_size = ast.literal_eval(SETTINGS['mainframe_size']['min_size'])
        title = SETTINGS['mainframe_size']['title']
        
        self.SetSize(size)
        self.SetMinSize(min_size)
        self.SetTitle(title)
        
        self._init_ui()

        
    def _init_ui(self) -> None:
        MainPanel(self, self._manage_data, self._settings, self._color_themes, self._theme_name)
        
        # self.SetMenuBar(TopBarMenu(self, self._command))
        
        self.Bind(wx.EVT_CLOSE, self._on_close)
    
    def _on_close(self, event) -> None:
        sys.exit(0)
        

 