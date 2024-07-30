#!/usr/bin/env python3


import wx
import os
import sys

from GUI.base_panel import BasePanel
from GUI.modals.set_new_password import SetNewPasswordFrame
from GUI.modals.popups import select_file, message_popup
from manage_data.data_file import DataFile

class FirstLaunch(BasePanel):
    def __init__(self, parent, data_file: DataFile,  gui_settings: dict, color_themes: dict, current_theme: str) -> None:
        super().__init__(parent)
        
        self._parent = parent
        
        self._df = data_file
        self._gui_settings = gui_settings
        self._color_themes = color_themes 
        self._current_theme = current_theme
        
        self._config = self._gui_settings['first_launch']
        
        self.password_set = False
        
        self._init_ui()
        self._bind_events()
        
        self.applay_color_theme()
        
    def _init_ui(self) -> None:
        main_box = wx.BoxSizer(wx.VERTICAL)
        
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        
        self._create_new = wx.Button(self, label=self._config['create_new'])
        self._select_another_datafile = wx.Button(self, label=self._config['import_datafile'])
      
        button_box.Add(self._create_new)
        button_box.Add(self._select_another_datafile, 0, wx.LEFT, 20)

        main_box.Add(button_box, 1, wx.ALIGN_CENTER | wx.TOP, 90)
        
        self.SetSizer(main_box)
        self.Layout()
        
    def _bind_events(self) -> None:
        self._create_new.Bind(wx.EVT_BUTTON, self._on_create_new)
        self._select_another_datafile.Bind(wx.EVT_BUTTON, self._on_select_another_datafile)
        self.Bind(wx.EVT_CLOSE, self._on_close)
        
    def _on_create_new(self, event) -> None:
        self._new_password_frame = SetNewPasswordFrame(self, self._df, self._gui_settings, self._color_themes, self._current_theme)
        self._new_password_frame.Show() 
    
    def _on_select_another_datafile(self, event) -> None:
        new_file = select_file("data")
        if new_file is not None:
            self._df.change_datafile_path(new_file)
            message_popup(f"You have selected: '{new_file}'", "New DataFile Selected")
            self.GetParent().main_app.get_password()
            self.GetParent().Destroy()
    
    def close(self):
        self.GetParent().Destroy()
        
    def launch_main_app(self):
        self.GetParent().main_app.LaunchMainApp()
    
    def applay_color_theme(self):
        self.SetBackgroundColour(wx.Colour(self._color_themes[self._current_theme]['dark']))
        
    def _on_close(self, event) -> None:
        os._exit(0)


class FirstLaunchFrame(wx.Frame):
    def __init__(self, data_file: DataFile, gui_settings: dict, color_themes: dict, current_theme: str, main_app: wx.App):
        super().__init__(None, style=wx.CLOSE_BOX, title=gui_settings['global']['app_name'])
        
        self._df = data_file
        self._gui_settings = gui_settings
        self._color_themes = color_themes 
        self._current_theme = current_theme
        self.main_app = main_app
        
        self.CenterOnScreen()
        self._init_ui()
        
    def _init_ui(self):
        
        panel = FirstLaunch(self, self._df, self._gui_settings, self._color_themes, self._current_theme)
    


    

