#!/usr/bin/env python3



import wx
import os
import sys



class SetNewPassword(wx.Frame):
    def __init__(self, data_file: DataFile, settings: Settings, change_password: bool = False) -> None:

        super().__init__(None, style=wx.CLOSE_BOX, title=SetNewPasswordConst.TITLE)
        
        self.SetBackgroundColour(ColourTheme.AVAILABLE_COLOUR_SCHEMES[settings.COLOUR_SCHEME].MID_PANEL)
        
        self._data_file = data_file
        self._settings = settings
        self._change_password = change_password
        
        self.CenterOnScreen()
        
        self._init_ui()
        self._bind_events()
        
        
    def _init_ui(self) -> None:
        panel = wx.Panel(self)
        
        main_box = wx.BoxSizer(wx.VERTICAL)
        
        new_password_box = wx.BoxSizer(wx.HORIZONTAL)
        confirm_new_password_box = wx.BoxSizer(wx.HORIZONTAL)
        password_strength_box = wx.BoxSizer(wx.HORIZONTAL)
        buttons_box = wx.BoxSizer(wx.HORIZONTAL)
        
        self._new_password = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER | wx.TE_PASSWORD, size=SetNewPasswordConst.INPUT_FIELD_SIZE)
        self._new_password.SetHint(SetNewPasswordConst.NEW_PASSOWRD_HINT)
        self._new_password.SetFocus()
        
        self._confirm_new_password = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER | wx.TE_PASSWORD, size=SetNewPasswordConst.INPUT_FIELD_SIZE)
        self._confirm_new_password.SetHint(SetNewPasswordConst.CONFIRM_NEW_PASSWORD_HINT)
        
        self._cancel = wx.Button(panel, label=SetNewPasswordConst.CANCEL_LABEL)
        self._confirm = wx.Button(panel, label=SetNewPasswordConst.CONFIRM_LABEL)
        
        new_password_box.Add(self._new_password)
        confirm_new_password_box.Add(self._confirm_new_password)
        
        buttons_box.Add(self._cancel)
        buttons_box.Add(self._confirm, 0, wx.LEFT, 30)
        
        main_box.Add(new_password_box, 0, wx.ALIGN_CENTER | wx.TOP, 60)
        main_box.Add(confirm_new_password_box, 0, wx.ALIGN_CENTER | wx.TOP, SetNewPasswordConst.DISTANCE_BETWEEN_BUTTONS)
        
        main_box.Add(password_strength_box, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        
        main_box.Add(buttons_box, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        
        panel.SetSizer(main_box)
        panel.Layout()
        
        
    def _bind_events(self) -> None:
        self._confirm.Bind(wx.EVT_BUTTON, self._on_confirm)
        self._cancel.Bind(wx.EVT_BUTTON, self._on_cancel)
        self._new_password.Bind(wx.EVT_TEXT_ENTER, self._on_new_password_enter)
        self._confirm_new_password.Bind(wx.EVT_TEXT_ENTER, self._on_confirm_new_password_enter)
        
    def _on_new_password_enter(self, event) -> None:
        password = self._new_password.GetValue()
        if len(password) == 0:
            message_popup(EmptyFieldPopup.TITLE, EmptyFieldPopup.MESSAGE)
            self._new_password.SetFocus()
            return 
        self._confirm_new_password.SetFocus()
        
    def _on_confirm_new_password_enter(self, event) -> None:
        self._on_confirm(None)
        
    def _on_confirm(self, event) -> None:
        password = self._new_password.GetValue()
        confirmation = self._confirm_new_password.GetValue()
        if not password == confirmation:
            message_popup(PasswordDoesNotMatchPopup.MESSAGE, PasswordDoesNotMatchPopup.TITLE)
            self._new_password.SetValue("")
            self._confirm_new_password.SetValue("")
            self._new_password.SetFocus()
            return 
        self._data_file.password = password
        if self._change_password:
            self._data_file.commit()
        else:
            self._data_file.create()
        message_popup(PasswordCreatedPopup.MESSAGE, PasswordCreatedPopup.TITLE)
        self._restart()
        
    def _restart(self) -> None:
        python = sys.executable
        os.execl(python, python, * sys.argv)
             
    def _on_cancel(self, event) -> None:
        self.Close()


def launch_set_new_password(data_file: DataFile, settings: Settings, change_password: bool = False):
    app = wx.App()
    SetNewPassword(data_file, settings, change_password).Show()
    app.MainLoop()
















