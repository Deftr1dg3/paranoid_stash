#!/usr/bin/env python3



import wx
import pyperclip
from pathlib import Path

from manage_data import DataFile
from manage_data.aes_encryption import AES_Encripton
from GUI.base_panel import BasePanel
from GUI.modals.popups import message_popup, select_file, save_file_as, dialog_popup
from GUI.modals.copy_popup import CopyPopup

# import logging 

# Custom file handler that flushes after each log message
# Custom stream handler that flushes after each log message
# class FlushStreamHandler(logging.StreamHandler):
#     def __init__(self, stream=None):
#         super().__init__(stream)
#         self.setLevel(logging.DEBUG)
#         self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
#     def emit(self, record):
#         super().emit(record)
#         self.flush()

# # Set up logging to use FlushStreamHandler writing to a file
# log_file = open("app.log", "a", buffering=1)
# handler = FlushStreamHandler(stream=log_file)
# logging.basicConfig(level=logging.DEBUG, handlers=[handler])



class FileEncryption(BasePanel):
    def __init__(self, parent: wx.Frame) -> None:
        super().__init__(parent)
        
        # self._parent = parent
        
        # self._df = data_file
        # self._settings = settings
        # self._color_themes = color_themes 
        # self._current_theme = current_theme
        
        self._config = self._settings['file_encryption']
        self._aes_encryption = AES_Encripton()
        
        self._init_ui()
        self._bind_events()
        
        self.applay_color_theme()
    
    def _init_ui(self) -> None:
        
        main_box = wx.BoxSizer(wx.VERTICAL)
        
        file_path_box = wx.BoxSizer(wx.HORIZONTAL)
        save_as_box = wx.BoxSizer(wx.HORIZONTAL)
        password_box = wx.BoxSizer(wx.HORIZONTAL)
        buttons_box = wx.BoxSizer(wx.HORIZONTAL)
        
        self._file = wx.TextCtrl(self, size=self._config['input_field_size'])
        self._brows = wx.Button(self, label=self._config['brows_label'])
        self._file.SetHint(self._config['file_hint'])
        
        self._save_as = wx.TextCtrl(self, size=self._config['input_field_size'], style=wx.TE_READONLY)
        self._save_as.SetEditable(False)
        self._copy_save_as = wx.Button(self, label=self._config['copy_label'])
        self._save_as.SetHint(self._config['save_as_hint'])
        
        self._password = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER | wx.TE_PASSWORD, size=self._config['input_field_size'])
        self._copy = wx.Button(self, label=self._config['copy_label'])
        self._password.SetHint(self._config['password_hint'])
        
        self._decrypt = wx.Button(self, label=self._config['decrypt_label'])
        self._encrypt = wx.Button(self, label=self._config['encrypt_label'])
        
        file_path_box.Add(self._file, 0, wx.RIGHT, 10)
        file_path_box.Add(self._brows, 0, wx.TOP, 2)
        
        save_as_box.Add(self._save_as, 0, wx.RIGHT, 10)
        save_as_box.Add(self._copy_save_as, 0, wx.TOP, 2)
        
        password_box.Add(self._password, 0, wx.RIGHT, 10)
        password_box.Add(self._copy, 0, wx.TOP, 2)
        
        buttons_box.Add(self._decrypt)
        buttons_box.Add(self._encrypt, 0, wx.LEFT, 40)
        
        main_box.Add(file_path_box, 0, wx.ALIGN_CENTER | wx.TOP, 30)
        main_box.Add(save_as_box, 0, wx.ALIGN_CENTER | wx.TOP, 15)
        main_box.Add(password_box, 0, wx.ALIGN_CENTER | wx.TOP, 30)
        
        main_box.Add(buttons_box, 0, wx.ALIGN_CENTER | wx.TOP, 30)
        
        self.SetSizer(main_box)
        self.Layout()
        
    def _bind_events(self) -> None:
        
        self._decrypt.Bind(wx.EVT_BUTTON, self._on_decrypt)
        self._encrypt.Bind(wx.EVT_BUTTON, self._on_encrypt)
        
        self._brows.Bind(wx.EVT_BUTTON, self._on_brows)
        self._copy.Bind(wx.EVT_BUTTON, self._on_copy)
        self._copy_save_as.Bind(wx.EVT_BUTTON, self._on_copy_save_as)
    
    def _validate_path_and_password(self) -> tuple[Path, str]:
        file_path = self._file.GetValue()
        # save_as = self._save_as.GetValue()
        password = self._password.GetValue()
        if not file_path:
            raise ValueError("No file selected")
        else:
            path = Path(file_path)
            if path.is_dir():
                raise ValueError("Directory selected instead of single file.")
            if not path.exists():
                raise ValueError("File does not exist.")
        if not password:
            raise ValueError("No password provided.")
        return path, password
            
    def _on_brows(self, event) -> None:
        file_path = select_file()
        if file_path is not None:
            self._file.SetValue(file_path)
        
    def _on_copy(self, event: wx.Event) -> None:
        password = self._password.GetValue()
        if password:
            pyperclip.copy(password)
            copy_indicator = CopyPopup(self)
            copy_indicator.Show()
        
    def _on_copy_save_as(self, event: wx.Event) -> None:
        save_as_path = self._save_as.GetValue()
        if save_as_path:
            pyperclip.copy(save_as_path)
            copy_indicator = CopyPopup(self)
            copy_indicator.Show()
            
    def encryption(self, file_path: Path, password: str, decrypt: bool = False) -> bytes:
        with open(file_path, 'rb') as f:
            data_bytes = f.read()
        if not decrypt:
            result_bytes = self._aes_encryption.encrypt(password, data_bytes)
        else:
            try:
                result_bytes = self._aes_encryption.decrypt(password, data_bytes)
            except ValueError:
                raise
        return result_bytes
    
    
    def save_data_bytes(self, data: bytes, save_as: Path) -> None:
        if save_as.exists():
            confirmed = dialog_popup(message=self.settings['popup']['file_already_exists']['message'].format(save_as), title=self.settings['popup']['file_already_exists']['title'])
            if not confirmed:
                return
        try:
            with open(save_as, 'wb') as f:
                    f.write(data)
        except Exception as ex:
                message_popup(message=self.settings['popup']['message']['exception'].format(ex), title=self.settings['popup']['error']['title'])
        else:
            message_popup(message=self.settings['popup']['message']['file_saved'].format(save_as), title=self.settings['popup']['success']['title'])
        
        
    def _on_encrypt(self, event: wx.Event) -> None:
        try:
            file_path, password = self._validate_path_and_password()
        except ValueError as ex:
            message_popup(message=f"{ex}", title=self.settings['popup']['error']['title'])
        else:
            save_as = Path(str(file_path) + self._config['encrypted_extension'])
            self._save_as.SetValue(str(save_as))
            try:
                encrypted_bytes = self.encryption(file_path=file_path, password=password)
            except Exception as ex:
                message_popup(message=self.settings['popup']['message']['exception'].format(ex), title=self.settings['popup']['error']['title'])
            else:
                self.save_data_bytes(encrypted_bytes, save_as)
              
        
    def _on_decrypt(self, event: wx.Event) -> None:
        try:
            file_path, password = self._validate_path_and_password()
        except ValueError as ex:
            message_popup(message=f"{ex}", title=self.settings['popup']['error']['title'])
        else:
            extension = '.' + str(file_path).split('.')[-1]
            if extension != self._config['encrypted_extension']:
                message_popup(message=self.settings['popup']['message']['wrong_extension'].format(self._config['encrypted_extension'], extension), title=self.settings['popup']['error']['title'])
                return
            directory = file_path.parent
            save_as = directory / file_path.stem
            try:
                decrypted_bytes = self.encryption(file_path=file_path, password=password, decrypt=True)
            except ValueError:
                another_try = dialog_popup(self.settings['get_password']['wrong_password']['message'], self.settings['get_password']['wrong_password']['title'], yes_default=True)
                if not another_try:
                    self._on_cancel()
                return 
            except Exception as ex:
                message_popup(message=self.settings['popup']['message']['exception'].format(ex), title=self.settings['popup']['error']['title'])
            else:
                self.save_data_bytes(decrypted_bytes, save_as)
                
                
    def _on_cancel(self, event: wx.Event | None = None):
        self.GetParent().Destroy()
    
    
    def applay_color_theme(self):
        self._text_colour = self._color_themes[self._current_theme]['text']
        self._input_background_colour = self._color_themes[self._current_theme]['input_background']
        
        self._file.SetForegroundColour(self._text_colour)
        self._save_as.SetForegroundColour(self._text_colour)
        self._password.SetForegroundColour(self._text_colour)
        
        self._file.SetBackgroundColour(self._input_background_colour )
        self._save_as.SetBackgroundColour(self._input_background_colour )
        self._password.SetBackgroundColour(self._input_background_colour )
        
        self.SetBackgroundColour(self._color_themes[self._current_theme]['dark'])
        
        self.Refresh()


class FileEncryptionFrame(wx.Frame):
    def __init__(self, parent: BasePanel, gui_settings: dict) -> None:
        
        super().__init__(parent, style=wx.CLOSE_BOX, title=gui_settings['file_encryption']['title'])
        
        
        self.CenterOnScreen()
        self._init_ui()
        
    def _init_ui(self) -> None:
        panel = FileEncryption(self)
        

















