#!/usr/bin/env python3

import wx
import random
import ast
from itertools import cycle

from manage_data import ManageData, DataFile
from manage_data import GeneratePassword, ValidatePassword, PasswordStrength

from GUI.base_panel import BasePanel

class TopMidPanel(BasePanel):
    def __init__(self, parent: wx.Panel, manage_date: ManageData, settings: dict, color_themes: dict, theme_name: str) -> None:
        self._parent = parent 
        self._manage_data = manage_date
        self._settings = settings
        self.color_themes = color_themes
        self.theme_name = theme_name
        
        self._search_field_size = ast.literal_eval(self._settings['top_panel']['top_mid_panel']['search_field_size'])
        self._new_entry_label = self._settings['top_panel']['top_mid_panel']['new_entry_label']
        self._search_placeholder = self._settings['top_panel']['top_mid_panel']['search_placeholder']
        
        self._foreground_color = wx.Colour(self.color_themes[self.theme_name]['text'])
        
        super().__init__(parent)
        
        self._init_ui()
        self._bind_events()
        
        self.applay_color_theme(self.theme_name)
        
    def _init_ui(self) -> None:
        # Create main sizer
        main_box = wx.BoxSizer(wx.HORIZONTAL)
        
        # Create secondary sizers, that will be added to the main sizer.
        button_box = wx.BoxSizer(wx.VERTICAL)
        search_box = wx.BoxSizer(wx.VERTICAL)
        
        self._new_entry = wx.Button(self, label=self._new_entry_label)
        # self._new_entry = wx.StaticText(self, label=self._new_entry_label)

        self._search = wx.TextCtrl(self, size=self._search_field_size, style=wx.TE_PROCESS_ENTER)
        self._search.SetHint(self._search_placeholder)

        # Add created objects to the sizers
        button_box.Add(self._new_entry, 0, wx.EXPAND | wx.LEFT, 10)
        search_box.Add(self._search, 0, wx.EXPAND)
        
        # Add sizers to the main sizer.
        main_box.Add(button_box, 0, wx.ALL | wx.EXPAND, 5)
        main_box.AddStretchSpacer()
        
        main_box.Add(search_box, 0, wx.ALL | wx.EXPAND, 3)
        
        # Set main sizer to the panel
        self.SetSizer(main_box)
        
        # Refresh layout
        self.Layout()
        
        self._dummy_panel = wx.Panel(self, size=(0, 0))
        
    def _bind_events(self) -> None:
        self._new_entry.Bind(wx.EVT_BUTTON, self._add_entry)
        self._search.Bind(wx.EVT_TEXT, self._on_search)
        self._search.Bind(wx.EVT_TEXT_ENTER, self._on_enter_pressed)
    
    def _on_enter_pressed(self, event):
        self.deselect_search()
        event.Skip()
        
    def deselect_search(self):
        self._dummy_panel.SetFocus()

    def _add_entry(self, event) -> None:
        if self._manage_data.add_entry():
            self.body.mid_panel.refresh() # type: ignore
            self.body.right_panel.refresh() # type: ignore
        
    def _on_search(self, event) -> None:
        query = self._search.GetValue()
        self._manage_data.search(query)
        self._manage_data.selected_category = None 
        self._manage_data.selected_entry = None 
        
        self.body.left_panel.refresh() # type: ignore
        self.body.mid_panel.refresh() # type: ignore
        self.body.right_panel.refresh() # type: ignore
        
    
        
    def applay_color_theme(self, theme_name: str):
        self.theme_name = theme_name
        self.SetBackgroundColour(wx.Colour(self.color_themes[self.theme_name]['medium']))
        # self.SetBackgroundColour('red')
        # Foreground color works only woth Static Text ----------------------------------------
        self._search.SetForegroundColour(wx.Colour(self.color_themes[self.theme_name]['text']))
        # self._new_entry.SetForegroundColour(wx.Colour(self.color_themes[self.theme_name]['text']))
        self._search.SetBackgroundColour(wx.Colour(self.color_themes[self.theme_name]['input_background']))
        self.Refresh()