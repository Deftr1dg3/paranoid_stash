#!/usr/bin/env python3


import wx 
import ast

from manage_data import ManageData
from manage_data.manage_password.manage_password import ValidatePassword, GeneratePassword, PasswordStrength
from GUI.base_panel import BasePanel
from GUI.modals.popups import dialog_popup

from dataclasses import dataclass

@dataclass
class EntryFields:
    RECORD_NAME = 0
    USERNAME = 1
    PASSWORD = 2
    URL = 3
    NOTES = 4
    
STRENGTH_TYPES = {
    'VERY STRONG': PasswordStrength.VERY_STRONG,
    'STRONG': PasswordStrength.STRONG,
    'MEDIUM': PasswordStrength.MEDIUM,
    'WEAK': PasswordStrength.WEAK,
    'VERY WEAK': PasswordStrength.VERY_WEAK
}


class EditPanel(BasePanel):
    def __init__(self, parent: BasePanel) -> None:
        super().__init__(parent)
        
        self._show_password_ind = False
        self._show_password_label = self._settings['right_panel']['show_password_button_label']
        self._hide_password_label = self._settings['right_panel']['hide_password_button_label']
        self._generate_password_label = self._settings['right_panel']['generate_password_button_label']
        # self._PASSWORD_STRENGTH_OPTIONS = self._settings['right_panel']['password_strength_options']
        self._remove_entry_label = self._settings['right_panel']['remove_entry_button_label']
        self._placeholder = self._settings['right_panel']['entry_placeholder']
        
        self._dropdown_options = self._settings['right_panel']['password_strength_options'].split(',')
        self._current_password_strength = self._settings['right_panel']['defalut_password_strength']
        
        self._record_name_title = self._settings['right_panel']['record_name_title']
        self._username_title = self._settings['right_panel']['username_title']
        self._password_title = self._settings['right_panel']['password_title']
        self._url_title = self._settings['right_panel']['url_title']
        
        self._text_colour = self._color_themes[self._current_theme]['text']
        self._input_background_colour = self._color_themes[self._current_theme]['input_background']
        
        self._password_validator = ValidatePassword()
        
        # Initializing visible objects and binding events
        self._init_ui()
        self._bind_events()
        
        self.applay_color_theme()
        
    def _init_ui(self):
        """ Function initializing visible interface. """
        
        # Create main sizer
        main_box = wx.BoxSizer(wx.VERTICAL)
        
        # Create ScrolledWindow
        self._scroll = wx.ScrolledWindow(self, -1)
        self._scroll.SetScrollbars(20, 20, 50, 50)
        
        # Sizer for ScrolledWindow.
        self._scroll_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create GUI objects
        self._record_name_title = wx.StaticText(self._scroll, label=self._record_name_title)
        self._record_name = wx.TextCtrl(self._scroll, style=wx.TE_PROCESS_ENTER)
        
        self._username_title = wx.StaticText(self._scroll, label=self._username_title)
        self._username = wx.TextCtrl(self._scroll, style=wx.TE_PROCESS_ENTER)

        self._password_title = wx.StaticText(self._scroll, label=self._password_title)
        self._password = wx.TextCtrl(self._scroll, style=wx.TE_PROCESS_ENTER | wx.TE_PASSWORD)

        self._reveal_password = wx.Button(self._scroll, label=self._show_password_label)
        self._password_strength = wx.ComboBox(self._scroll, choices=self._dropdown_options, style=wx.CB_READONLY)
        self._generate_password_button = wx.Button(self._scroll, label=self._generate_password_label)
        
        self._url_title = wx.StaticText(self._scroll, label=self._url_title)
        self._url = wx.TextCtrl(self._scroll, style=wx.TE_PROCESS_ENTER)

        self._remove_entry = wx.Button(self._scroll, label=self._remove_entry_label)
        
        # Add GUI objects to the ScrolledWindow sizer
        self._scroll_sizer.Add(self._record_name_title, 0, wx.EXPAND | wx.ALL, 5)
        self._scroll_sizer.Add(self._record_name, 0, wx.EXPAND | wx.ALL, 5)
        self._scroll_sizer.Add(self._username_title, 0, wx.EXPAND | wx.ALL, 5)
        self._scroll_sizer.Add(self._username, 0, wx.EXPAND | wx.ALL, 5)
        self._scroll_sizer.Add(self._password_title, 0, wx.EXPAND | wx.ALL, 5)
        self._scroll_sizer.Add(self._password, 0, wx.EXPAND | wx.ALL, 5)
        self._scroll_sizer.Add(self._reveal_password, 0, wx.EXPAND | wx.ALL, 5)
        self._scroll_sizer.Add(self._password_strength, 0, wx.EXPAND | wx.ALL, 5)
        self._scroll_sizer.Add(self._generate_password_button, 0, wx.EXPAND | wx.ALL, 5)
        self._scroll_sizer.Add(self._url_title, 0, wx.EXPAND | wx.ALL, 5)
        self._scroll_sizer.Add(self._url, 0, wx.EXPAND | wx.ALL, 5)
        self._scroll_sizer.Add(self._remove_entry, 0, wx.EXPAND | wx.ALL, 5)
        
        # Alter GUI objects depending if an EntryRow was selected or not
        self.entry = self._manage_data.get_selected_entry()
        
        if self.entry is None:
            self._record_name.Disable()
            self._username.Disable()
            self._password.Disable()
            self._reveal_password.Disable()
            self._password_strength.Disable()
            self._generate_password_button.Disable()
            self._url.Disable()
            self._record_name.SetValue(self._placeholder)
            self._username.SetValue(self._placeholder)
            self._password.SetValue(self._placeholder)
            self._url.SetValue(self._placeholder)
            self._remove_entry.Disable()
        else:
            entry_name = self.entry[EntryFields.RECORD_NAME]
            username = self.entry[EntryFields.USERNAME]
            password = self.entry[EntryFields.PASSWORD]
            url = self.entry[EntryFields.URL]
            self._record_name.SetValue(entry_name)
            self._record_name.SetInsertionPointEnd()
            self._record_name.SetFocus()
            self._username.SetValue(username)
            self._password.SetValue(password)
            self._validate_password_strength(None)
            self._url.SetValue(url)
            

        # Set sizer to the ScrolledWindow
        self._scroll.SetSizer(self._scroll_sizer)
        
        # Add Scrolled Window to the main sizer
        main_box.Add(self._scroll, 1, wx.EXPAND)
        
        # Set the main sizer to the panel
        self.SetSizer(main_box)
        
        # Refresh layout
        self.Layout()
        
        # Create dummy element to Kill Focus in main elements
        self._dummy_panel = wx.Panel(self, size=(0, 0))
        
        
    def _bind_events(self):
        self._record_name.Bind(wx.EVT_TEXT, self._on_record_name)
        self._username.Bind(wx.EVT_TEXT, self._on_username)
        self._password.Bind(wx.EVT_TEXT, self._on_password)
        self._url.Bind(wx.EVT_TEXT, self._on_url)
        
        self._record_name.Bind(wx.EVT_TEXT_ENTER, self._on_enter_pressed)
        self._username.Bind(wx.EVT_TEXT_ENTER, self._on_enter_pressed)
        self._password.Bind(wx.EVT_TEXT_ENTER, self._on_enter_pressed)
        self._url.Bind(wx.EVT_TEXT_ENTER, self._on_enter_pressed)
        
        self._reveal_password.Bind(wx.EVT_BUTTON, self._on_show_password)
        self._generate_password_button.Bind(wx.EVT_BUTTON, self._on_generate_password)
        self._password_strength.Bind(wx.EVT_COMBOBOX, self._on_select_password_strength)
        self._remove_entry.Bind(wx.EVT_BUTTON, self._on_remove_entry)
        
        # self._record_name.Bind(wx.EVT_SET_FOCUS, self._on_set_focus)
        # self._username.Bind(wx.EVT_SET_FOCUS, self._on_set_focus)
        # self._password.Bind(wx.EVT_SET_FOCUS, self._on_set_focus)
        # self._url.Bind(wx.EVT_SET_FOCUS, self._on_set_focus)
       
    def _on_enter_pressed(self, event) -> None:
        obj = event.GetEventObject()
        if obj.HasFocus():
            self._dummy_panel.SetFocus()
            self._manage_data.save_state()
            
    # def _on_set_focus(self, event) -> None:
    #     self._undo_available = True
    
    def deselect_all(self):
        self._dummy_panel.SetFocus()

    def _on_record_name(self, event) -> None:
        if self.entry == None:
            return
        value = self._record_name.GetValue()
        self.entry[EntryFields.RECORD_NAME] = value
        self._on_enter(None)

    def _on_username(self, event) -> None:
        if self.entry == None:
            return
        value = self._username.GetValue()
        self.entry[EntryFields.USERNAME] = value
        self._on_enter(None)
    
    def _on_password(self, event) -> None:
        if self.entry == None:
            return
        value = self._password.GetValue()
        self.entry[EntryFields.PASSWORD] = value
        self._validate_password_strength(None)
        self._on_enter(None)
    
    def _on_url(self, event) -> None:
        if self.entry == None:
            return
        value = self._url.GetValue()
        self.entry[EntryFields.URL] = value
        self._on_enter(None)
        
    def _on_enter(self, event) -> None:
        self._manage_data.update()
        self._manage_data.save_state()
        self.refresh_mid_panel()
    
    def _on_remove_entry(self, event):
        title = self._settings['right_panel']['remove_entry']['title']
        message = self._settings['right_panel']['remove_entry']['message']
        confirmed = dialog_popup(message, title)
        if confirmed:
            self._manage_data.delete_entry()
            self.refresh_mid_panel()
            self.refresh_right_panel()
            self._on_enter
        
    def _validate_password_strength(self, event) -> None:
        if self.entry == None:
            return
        password = self.entry[2]
        result = self._password_validator.validate_password(password)
        self._current_password_strength = result 
        self._password_strength.SetValue(self._current_password_strength)
        
    def _on_select_password_strength(self, event) -> None:
        self._current_password_strength = self._password_strength.GetValue()
    
    def _on_generate_password(self, event) -> None:
        if self.entry is None:
            return
        title = self._settings['right_panel']['new_password']['title']
        message = self._settings['right_panel']['new_password']['message']
        confirmed = dialog_popup(message, title)
        if confirmed:
            g = GeneratePassword()
            password = g.generate_password(STRENGTH_TYPES[self._current_password_strength])  
            self._password.SetValue(password)
            self.entry[EntryFields.PASSWORD] = password
            self._on_enter(None)
            
        
    def _on_show_password(self, event):
        if self.entry is None:
            return
        if not self._show_password_ind:
            self._show_password_ind = not self._show_password_ind
            self._on_password(None)
            self._password.Destroy()
            self._password = wx.TextCtrl(self._scroll, style=wx.TE_PROCESS_ENTER)
            self._password.Bind(wx.EVT_TEXT_ENTER, self._on_enter)
            self._password.Bind(wx.EVT_KILL_FOCUS, self._on_enter)
            self._password.Bind(wx.EVT_TEXT, self._on_password)
            self._password.SetForegroundColour(self._text_colour)
            self._password.SetBackgroundColour(self._input_background_colour)
            self._scroll_sizer.Insert(5, self._password, 0, wx.EXPAND | wx.ALL, 5)
            self._password.SetValue(self.entry[EntryFields.PASSWORD])
            self._reveal_password.SetLabel(self._hide_password_label)
            self.Layout()
        else:
            self._show_password_ind = not self._show_password_ind
            self._on_password(None)
            self._password.Destroy()
            self._password = wx.TextCtrl(self._scroll, style=wx.TE_PROCESS_ENTER | wx.TE_PASSWORD)
            self._password.Bind(wx.EVT_TEXT_ENTER, self._on_enter)
            self._password.Bind(wx.EVT_KILL_FOCUS, self._on_enter)
            self._password.Bind(wx.EVT_TEXT, self._on_password)
            self._password.SetForegroundColour(self._text_colour)
            self._password.SetBackgroundColour(self._input_background_colour)
            self._scroll_sizer.Insert(5, self._password, 0, wx.EXPAND | wx.ALL, 5)
            self._password.SetValue(self.entry[EntryFields.PASSWORD])
            self._reveal_password.SetLabel(self._show_password_label)
            self.Layout()
        
    def applay_color_theme(self):
        self._text_colour = self._color_themes[self._current_theme]['text']
        self._input_background_colour = self._color_themes[self._current_theme]['input_background']
        
        self._record_name.SetForegroundColour(self._text_colour)
        self._username.SetForegroundColour(self._text_colour)
        self._password.SetForegroundColour(self._text_colour)
        self._password_strength.SetForegroundColour(self._text_colour)
        self._url.SetForegroundColour(self._text_colour)
        
        self._record_name_title.SetForegroundColour(self._text_colour)
        self._username_title.SetForegroundColour(self._text_colour)
        self._password_title.SetForegroundColour(self._text_colour)
        self._url_title.SetForegroundColour(self._text_colour)
        
        self.Refresh()