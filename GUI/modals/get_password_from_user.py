#!/usr/bin/env python3


import wx 
import os
import sys
from data_file import DataFile
from settings import Settings
from gui.modals.popups import dialog_popup, message_popup
from exceptions import UnableToDecodeTheFile
from gui.colours import ColourTheme
from gui.modals.popups import select_file
from config import PasswordWindowConst, GeneralConst, WrongExtensionPopup, EmptyFieldPopup

class SetPassword(wx.Frame):
    def __init__(self, data_file: DataFile, settings: Settings) -> None:
        super().__init__(None, style=PasswordWindowConst.STYLE, size=PasswordWindowConst.SIZE, title=GeneralConst.APP_NAME)
        
        self.SetBackgroundColour(ColourTheme.AVAILABLE_COLOUR_SCHEMES[settings.COLOUR_SCHEME].MID_PANEL)
        
        self._data_file = data_file
        self._settings = settings
        
        self.CenterOnScreen()
        
        self._init_ui()
        self._bind_events()
        
        
    def _init_ui(self) -> None:
        panel = wx.Panel(self)
        
        main_box = wx.BoxSizer(wx.VERTICAL)
        
        input_box = wx.BoxSizer(wx.HORIZONTAL)
        buttons_box = wx.BoxSizer(wx.HORIZONTAL)
        
        self._password = wx.TextCtrl(panel, style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER, size=(200, -1))
        self._password.SetHint(PasswordWindowConst.PASSOWRD_HINT)
        self._password.SetFocus()
        
        self._choose_datafile = wx.Button(panel, label=PasswordWindowConst.SELECT_DATAFILE_LABEL)
        
        input_box.Add(self._password, 1, wx.ALIGN_CENTER)

        main_box.Add(input_box, 1, wx.ALIGN_CENTER)
        main_box.Add(buttons_box, 1, wx.EXPAND)
        
        panel.SetSizer(main_box)
        panel.Layout()
        
        
    def _bind_events(self) -> None:
        self._choose_datafile.Bind(wx.EVT_BUTTON, self._on_choose_another_datafile)
        self._password.Bind(wx.EVT_TEXT_ENTER, self._on_key_down)
        self.Bind(wx.EVT_CLOSE, self._on_close)

        
    def _on_key_down(self, event) -> None:
        self._on_confirm(None)
        
    def _on_confirm(self, event) -> None:
        password = self._password.GetValue()
        if len(password) == 0:
            message_popup(EmptyFieldPopup.TITLE, EmptyFieldPopup.MESSAGE)
            self._password.SetFocus()
            return 
        try:
            self._data_file.password = password
            self._data_file.load_data()
            self.Destroy()
        except UnableToDecodeTheFile:
            another_try = dialog_popup(PasswordWindowConst.DIALOG_MESSAGE, PasswordWindowConst.DIALOG_TITLE, yes_default=True)
            if not another_try:
                os._exit(0)
            self._password.SetValue("")
        
    def _on_clear(self, event) -> None:
        self._password.SetValue("")
        
    def _on_choose_another_datafile(self, event) -> None:
        file_path = select_file()
        if file_path is not None:
            valid = self._validate_path(file_path)
            if valid:
                self._settings.DATAFILE_PATH = file_path
                self.restart()
                
    def _validate_path(self, path: str) -> bool:
        file_name, extension = os.path.splitext(path)
        if extension == GeneralConst.DATAFILE_EXTENSION:
            return True
        proceed = dialog_popup(WrongExtensionPopup.MESSAGE, WrongExtensionPopup.TITLE)
        if proceed:
            return True
        return False
    
    def restart(self) -> None:
        python = sys.executable
        os.execl(python, python, * sys.argv)
        
    def _on_close(self, event) -> None:
        os._exit(0)


def launch_get_password(data_file: DataFile, settings: Settings):
    app = wx.App()
    SetPassword(data_file, settings).Show()
    app.MainLoop()
    
