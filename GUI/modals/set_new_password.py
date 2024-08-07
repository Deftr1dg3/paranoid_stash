#!/usr/bin/env python3



import wx
import os
import sys
from pathlib import Path
from base64 import b64decode, b64encode

from manage_data import DataFile 
from manage_data.data_file import IODataFile
from manage_data.aes_encryption.aes import AES_Encripton
from GUI.base_panel import BasePanel
from GUI.modals.popups import message_popup

# import logging 

# log_format = "%(asctime)s - %(levelname)s - %(message)s"
# logging.basicConfig(filename="app.log", level=logging.DEBUG, format=log_format)


class SetNewPassword(BasePanel):
    def __init__(self, parent: wx.Frame, data_file: DataFile,  gui_settings: dict, color_themes: dict, current_theme: str, change_password: bool = False) -> None:
        super().__init__(parent)
        
        self._parent = parent
        
        self._df = data_file
        self._gui_settings = gui_settings
        self._change_password = change_password
        if not self._change_password:
            self._color_themes = color_themes 
            self._current_theme = current_theme
        
        self._aes_encryption = AES_Encripton()
        self._io = IODataFile(self._gui_settings)
        
        self._config = self._gui_settings['new_password']
        
        self._init_ui()
        self._bind_events()
        
        self.applay_color_theme()
    
    def _init_ui(self) -> None:
        
        main_box = wx.BoxSizer(wx.VERTICAL)
        
        new_password_box = wx.BoxSizer(wx.HORIZONTAL)
        confirm_new_password_box = wx.BoxSizer(wx.HORIZONTAL)
        password_strength_box = wx.BoxSizer(wx.HORIZONTAL)
        buttons_box = wx.BoxSizer(wx.HORIZONTAL)
        
        self._new_password = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER | wx.TE_PASSWORD, size=self._config['input_field_size'])
        self._new_password.SetHint(self._config['new_password_hint'])
        # self._new_password.SetFocus()
        
        self._confirm_new_password = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER | wx.TE_PASSWORD, size=self._config['input_field_size'])
        self._confirm_new_password.SetHint(self._config['confirm_password_hint'])
        
        self._cancel = wx.Button(self, label=self._config['cancel_label'])
        self._confirm = wx.Button(self, label=self._config['confirm_label'])
        
        new_password_box.Add(self._new_password)
        confirm_new_password_box.Add(self._confirm_new_password)
        
        buttons_box.Add(self._cancel)
        buttons_box.Add(self._confirm, 0, wx.LEFT, 30)
        
        main_box.Add(new_password_box, 0, wx.ALIGN_CENTER | wx.TOP, 60)
        main_box.Add(confirm_new_password_box, 0, wx.ALIGN_CENTER | wx.TOP, self._config['margin_buttons'])
        
        main_box.Add(password_strength_box, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        
        main_box.Add(buttons_box, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        
        self.SetSizer(main_box)
        self.Layout()
        
    def _bind_events(self) -> None:
        self._confirm.Bind(wx.EVT_BUTTON, self._on_confirm)
        self._cancel.Bind(wx.EVT_BUTTON, self._on_cancel)
        self._new_password.Bind(wx.EVT_TEXT_ENTER, self._on_new_password_enter)
        self._confirm_new_password.Bind(wx.EVT_TEXT_ENTER, self._on_confirm_new_password_enter)
        
    def _on_new_password_enter(self, event) -> None:
        password = self._new_password.GetValue()
        if len(password) == 0:
            message_popup(self._gui_settings['empy_field']['title'], self._gui_settings['empy_field']['message'])
            self._new_password.SetFocus()
            return 
        self._confirm_new_password.SetFocus()
        
    def _on_confirm_new_password_enter(self, event) -> None:
        self._on_confirm(None)
        
    def _on_confirm(self, event) -> None:
        password = self._new_password.GetValue()
        confirmation = self._confirm_new_password.GetValue()
        
        if not password == confirmation:
            message_popup(self._gui_settings['password_does_not_match']['message'], self._gui_settings['password_does_not_match']['title'])
            self._new_password.SetValue("")
            self._confirm_new_password.SetValue("")
            self._new_password.SetFocus()
            return 
        
        old_password = self._df.password
        self._df.password = password
        if self._change_password:
            try:
                self._df.save_data()
                message_popup("The new password has been applied successfully!", "Success.")
            except:
                message_popup("Unable to apply new password.", "Fail.")
            else:
                backups_list: list[Path] = self._df.list_backups()
                try:
                    for backup in backups_list:
                        b64_string = self._io.get_data(backup)
                        # logging.info(f"GOt data -> {b64_string}")
                        
                        encrypted_bytes_data = b64decode(b64_string)
                        # logging.info(f"GOt data -> {encrypted_bytes_data}")
                        
                        decrypted_bytes_data = self._aes_encryption.decrypt(old_password, encrypted_bytes_data)
                        # logging.info(f"Decrypted data -> {decrypted_bytes_data}")
                        
                        new_password_encrypted_bytes_data = self._aes_encryption.encrypt(self._df.password, decrypted_bytes_data)
                        # logging.info(f"Encrypted data -> {new_password_encrypted_bytes_data}")
                        
                        b64_encrypted_string = b64encode(new_password_encrypted_bytes_data).decode(self._settings['encoding'])
                        # logging.info(f"B64 data -> {new_password_encrypted_bytes_data}")
                        
                        self._io.save_data(b64_encrypted_string, backup)
                        # logging.info(f"Saved !!!")
                        
                except Exception as ex:
                    # logging.exception(f"EXCEPTION: {ex}")
                    message_popup(self._settings['popup']['message']['unable_update_backup_password'].format(ex), self._settings['popup']['error']['title'])
                else:
                    message_popup(self._settings['popup']['message']['applied_for_all_backups'], self._settings['popup']['info']['title'])
        else:
            self._df.create_new_data_file()
            message_popup(self._gui_settings['password_created']['message'], self._gui_settings['password_created']['title'])
            self.GetParent().parent.launch_main_app()
            self.GetParent().parent.close()
            
        self._on_cancel(None)

    def _on_cancel(self, event):
        self._parent.Destroy()
    
    def applay_color_theme(self):
        self._new_password.SetBackgroundColour(self._color_themes[self._current_theme]['input_background'])
        self._confirm_new_password.SetBackgroundColour(self._color_themes[self._current_theme]['input_background'])
        self.SetBackgroundColour(wx.Colour(self._color_themes[self._current_theme]['dark']))
        self.Refresh()


class SetNewPasswordFrame(wx.Frame):
    def __init__(self, parent: BasePanel,  data_file: DataFile,  gui_settings: dict, color_themes: dict, current_theme: str, change_password: bool = False) -> None:
        
        super().__init__(None, style=wx.CLOSE_BOX, title=gui_settings['new_password']['title'])
        
        self._df = data_file
        self._gui_settings = gui_settings
        self._color_themes = color_themes 
        self._current_theme = current_theme
        self._change_password = change_password
        self.parent = parent
        
        self.CenterOnScreen()
        self._init_ui()
        
    def _init_ui(self) -> None:
        panel = SetNewPassword(self, self._df, self._gui_settings, self._color_themes, self._current_theme, self._change_password)
        

















