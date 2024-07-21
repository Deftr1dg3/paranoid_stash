#!/usr/bin/env python3


import wx
import os
import sys
from data_file import DataFile
from settings import Settings
from gui.colours import ColourTheme
from gui.modals.popups import select_file, dialog_popup
from gui.modals.set_new_password import launch_set_new_password
from config import FirstLaunchConst, GeneralConst, WrongExtensionPopup


class FirstLaunch(wx.Frame):
    def __init__(self, data_file: DataFile, settings: Settings) -> None:
        super().__init__(None, style=wx.CLOSE_BOX, title=GeneralConst.APP_NAME)
        
        self.SetBackgroundColour(ColourTheme.AVAILABLE_COLOUR_SCHEMES[settings.COLOUR_SCHEME].MID_PANEL)
        
        self._data_file = data_file
        self._settings = settings
        
        self.CenterOnScreen()
        
        self._init_ui()
        self._bind_events()
        
        
    def _init_ui(self) -> None:
        panel = wx.Panel(self)
        
        main_box = wx.BoxSizer(wx.VERTICAL)
        
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        
        self._create_new = wx.Button(panel, label=FirstLaunchConst.CREATE_NEW_LABEL)
        self._import_datafile = wx.Button(panel, label=FirstLaunchConst.IMPORT_DATAFILE_LABEL)
      
        button_box.Add(self._create_new)
        button_box.Add(self._import_datafile, 0, wx.LEFT, 20)

        main_box.Add(button_box, 1, wx.ALIGN_CENTER | wx.TOP, 90)
        
        panel.SetSizer(main_box)
        panel.Layout()
        
        
    def _bind_events(self) -> None:
        self._create_new.Bind(wx.EVT_BUTTON, self._on_create_new)
        self._import_datafile.Bind(wx.EVT_BUTTON, self._on_import_datafile)
        
        
    def _on_create_new(self, event) -> None:
        launch_set_new_password(self._data_file, self._settings)
    
    
    def _on_import_datafile(self, event) -> None:
        new_file = select_file()
        if new_file is not None:
            self._settings.DATAFILE_PATH = new_file
            self._restart()
                
    
    def _import_file_to_default_path(self, file_path: str) -> None:
        default_datafile_path = self._data_file.datafile
        
        with open(file_path, "r", encoding="utf-8") as f:
            file_data = f.read()
            
        with open(default_datafile_path, "w", encoding="utf-8") as f:
            f.write(file_data)


    def _validate_path(self, path: str) -> bool:
        file_name, extension = os.path.splitext(path)
        if extension == GeneralConst.DATAFILE_EXTENSION:
            return True
        proceed = dialog_popup(WrongExtensionPopup.MESSAGE, WrongExtensionPopup.TITLE)
        if proceed:
            return True
        return False
    
    
    def _restart(self) -> None:
        python = sys.executable
        os.execl(python, python, * sys.argv)


def launch_first_start(data_file: DataFile, settings: Settings):
    app = wx.App()
    FirstLaunch(data_file, settings).Show()
    app.MainLoop()
    

