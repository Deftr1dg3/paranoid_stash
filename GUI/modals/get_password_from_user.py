#!/usr/bin/env python3


import wx
import sys
from pathlib import Path

from manage_data import DataFile
from GUI.base_panel import BasePanel
from GUI.modals.popups import message_popup, dialog_popup, select_file

from typing import Optional


class GetPassword(BasePanel):
    def __init__(self, parent: wx.Frame, data_file: DataFile,  gui_settings: dict, color_themes: dict, current_theme: str) -> None:
        super().__init__(parent)
         
        self._df = data_file
        self._gui_settings = gui_settings
        self._color_themes = color_themes 
        self._current_theme = current_theme
        
        self._config = self._gui_settings['get_password']
        
        self._init_ui()
        self._bind_events()
        
        self.applay_color_theme()
        
        
        
    def _init_ui(self) -> None:
        
        main_box = wx.BoxSizer(wx.VERTICAL)
        
        input_box = wx.BoxSizer(wx.HORIZONTAL)
        buttons_box = wx.BoxSizer(wx.HORIZONTAL)
        
        self._password = wx.TextCtrl(self, style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER, size=(200, -1))
        self._password.SetHint(self._config['password_hint'])
        self._password.SetFocus()
        
        self._choose_datafile = wx.Button(self, label=self._config['select_another_datafile'])
        
        input_box.Add(self._password, 1, wx.ALIGN_CENTER)

        main_box.Add(input_box, 1, wx.ALIGN_CENTER)
        main_box.Add(buttons_box, 1, wx.EXPAND)
        
        self.SetSizer(main_box)
        self.Layout()
        
    def _bind_events(self) -> None:
        self._choose_datafile.Bind(wx.EVT_BUTTON, self._on_choose_another_datafile)
        self._password.Bind(wx.EVT_TEXT_ENTER, self._on_key_down)
        self.Bind(wx.EVT_CLOSE, self._on_close)
        
    def _on_key_down(self, event) -> None:
        self._on_confirm(None)
        
    def _on_confirm(self, event) -> None:
        password = self._password.GetValue()
        if len(password) == 0:
            message_popup(self._config['no_password_provided']['title'], self._config['no_password_provided']['message'])
            self._password.SetFocus()
            return 
        try:
            self._df.password = password
            self._df.load_data()
        except ValueError:
            another_try = dialog_popup(self._config['wrong_password']['message'], self._config['wrong_password']['title'], yes_default=True)
            if not another_try:
                if not isinstance(self.GetParent().main_app, "wx.App"):
                    self.GetParent().main_app.restore_df()
                sys.exit(0)
            self._password.SetValue("")
        else:
            self.GetParent().main_app.LaunchMainApp()
            self.GetParent().Destroy()
        
    def _on_clear(self, event) -> None:
        self._password.SetValue("")
        
    def _on_choose_another_datafile(self, event) -> None:
        file_path = select_file("data")
        if file_path is not None:
            message_popup(f"You have selected: '{file_path}'", "New DataFile Selected")
            self._df.change_datafile_path(file_path)
        
    def applay_color_theme(self):
        self.SetBackgroundColour(wx.Colour(self._color_themes[self._current_theme]['dark']))
    
    def _on_close(self, event) -> None:
        sys.exit(0)



class GetPasswordFrame(wx.Frame):
    def __init__(self, data_file: DataFile,  gui_settings: dict, color_themes: dict, current_theme: str, main_app: wx.App | object) -> None:
        
        self._df = data_file
        self._gui_settings = gui_settings
        self._color_themes = color_themes 
        self._current_theme = current_theme
        self.main_app = main_app
        
        self._config = self._gui_settings['get_password']
        
        super().__init__(None, title=self._config['title'], style=wx.CLOSE_BOX, size=self._config['size'])
        
        self.CenterOnScreen()
        self._init_ui()

        
    def _init_ui(self):
        panel = GetPassword(self, self._df, self._gui_settings, self._color_themes, self._current_theme)
