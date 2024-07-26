#!/usr/bin/env python3


import wx
import os
import sys

from GUI.base_panel import BasePanel
from GUI.modals.set_new_password import SetNewPasswordFrame
from manage_data.data_file import DataFile

class FirstLaunch(BasePanel):
    def __init__(self, parent, data_file: DataFile,  gui_settings: dict, color_themes: dict, current_theme: str, main_app: wx.App) -> None:
        super().__init__(parent)
        
        self._parent = parent
        
        self._df = data_file
        self._gui_settings = gui_settings
        self._color_themes = color_themes 
        self._current_theme = current_theme
        self._main_app = main_app
        
        self._config = self._gui_settings['first_launch']
        
        self._init_ui()
        self._bind_events()
        
        self.applay_color_theme()
        
        
    def _init_ui(self) -> None:
        main_box = wx.BoxSizer(wx.VERTICAL)
        
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        
        self._create_new = wx.Button(self, label=self._config['create_new'])
        self._import_datafile = wx.Button(self, label=self._config['import_datafile'])
      
        button_box.Add(self._create_new)
        button_box.Add(self._import_datafile, 0, wx.LEFT, 20)

        main_box.Add(button_box, 1, wx.ALIGN_CENTER | wx.TOP, 90)
        
        self.SetSizer(main_box)
        self.Layout()
        
        
   
        
    def _bind_events(self) -> None:
        self._create_new.Bind(wx.EVT_BUTTON, self._on_create_new)
        self._import_datafile.Bind(wx.EVT_BUTTON, self._on_import_datafile)
        
        
    def _on_create_new(self, event) -> None:
        # launch_set_new_password(self._data_file, self._settings)
        self._new_password_frame = SetNewPasswordFrame(self._df, self._gui_settings, self._color_themes, self._current_theme, self._main_app, self._parent)
        self._new_password_frame.Show()
    
    
    def _on_import_datafile(self, event) -> None:
        # new_file = select_file()
        # if new_file is not None:
        #     self._settings.DATAFILE_PATH = new_file
        #     self._restart()
        ...
                
    
    def _import_file_to_default_path(self, file_path: str) -> None:
        # default_datafile_path = self._data_file.datafile
        
        # with open(file_path, "r", encoding="utf-8") as f:
        #     file_data = f.read()
            
        # with open(default_datafile_path, "w", encoding="utf-8") as f:
        #     f.write(file_data)
        ...


    def _validate_path(self, path: str) -> bool:
        # file_name, extension = os.path.splitext(path)
        # if extension == GeneralConst.DATAFILE_EXTENSION:
        #     return True
        # proceed = dialog_popup(WrongExtensionPopup.MESSAGE, WrongExtensionPopup.TITLE)
        # if proceed:
        #     return True
        # return False
        ...
    
    def applay_color_theme(self):
        self.SetBackgroundColour(wx.Colour(self._color_themes[self._current_theme]['medium']))


class FirstLaunchFrame(wx.Frame):
    def __init__(self, data_file: DataFile, gui_settings: dict, color_themes: dict, current_theme: str, main_app: wx.App):
        super().__init__(None, style=wx.CLOSE_BOX, title=gui_settings['global']['app_name'])
        
        self._df = data_file
        self._gui_settings = gui_settings
        self._color_themes = color_themes 
        self._current_theme = current_theme
        self._main_app = main_app
        
        self.CenterOnScreen()
        self._init_ui()
        
    def _init_ui(self):
        
        panel = FirstLaunch(self, self._df, self._gui_settings, self._color_themes, self._current_theme, self._main_app)
    


    

