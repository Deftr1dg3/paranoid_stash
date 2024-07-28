import sys 
import os 

import wx
import ast

from manage_data import ManageData
from GUI.main_panel import MainPanel
from GUI.top_bar_menu.menus import TopBarMenu

class MainFrame(wx.Frame):
    def __init__(self, manage_data: ManageData, gui_settings: dict, color_themes: dict, current_theme: str) -> None:
        super().__init__(None)
        
        self._manage_data = manage_data
        self._settings = gui_settings
        self._color_themes = color_themes
        self._theme_name = current_theme
        
        size = ast.literal_eval(self._settings['mainframe_size']['size'])
        min_size = ast.literal_eval(self._settings['mainframe_size']['min_size'])
        title = self._settings['mainframe_size']['title']
        
        self.SetSize(size)
        self.SetMinSize(min_size)
        self.SetTitle(title)
        
        self._init_ui()

        
    def _init_ui(self) -> None:
        main_panel = MainPanel(self, self._manage_data, self._settings, self._color_themes, self._theme_name)
        
        self.SetMenuBar(TopBarMenu(self, main_panel))
        
        self.Bind(wx.EVT_CLOSE, self._on_close)
    
    def _on_close(self, event) -> None:
        os._exit(0)
        

 