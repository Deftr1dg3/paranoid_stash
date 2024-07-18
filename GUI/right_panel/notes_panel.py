#!/usr/bin/env python3


import wx 
import ast

from manage_data import ManageData
from GUI.base_panel import BasePanel


class NotesPanel(BasePanel):
    def __init__(self, parent: wx.Panel, manage_date: ManageData, settings: dict, color_themes: dict, current_theme: str) -> None:
        self._parent = parent 
        self._manage_data = manage_date
        self._settings = settings
        self._color_themes = color_themes
        self._current_theme = current_theme
        
        self._title = self._settings['right_panel']['notes_title']
        self._notes_field_size = ast.literal_eval(self._settings['right_panel']['notes_field_size'])
        
        self._text_colour = self._color_themes[self._current_theme]['text']
        self._input_background_colour = self._color_themes[self._current_theme]['input_background']
        
        super().__init__(self._parent)
        
        # Initializing visible objects and binding events
        self._init_ui()
        self._bind_events()
        
        self.applay_color_theme(self._current_theme)
        
        
    def _init_ui(self):
        """ Function initializing visible interface. """
        
        # Create main sizer
        self._main_box = wx.BoxSizer(wx.VERTICAL)
        
        # Create secondary sizers
        title_box = wx.BoxSizer(wx.HORIZONTAL)
        notes_box = wx.BoxSizer(wx.HORIZONTAL)
        
        # Create GUI objects
        self._title = wx.StaticText(self, label=self._title)
        # self._title.SetForegroundColour(self._text_colour)
        self._notes = wx.TextCtrl(self, size=self._notes_field_size, style=wx.TE_MULTILINE)
        # self._notes.SetForegroundColour(self._text_colour)
        # self._notes.SetBackgroundColour(self._input_background_colour)
        
        # Enable or disable GUI objects depending on selected EntryRow
        # if self._command.selected_entry_row is None:
        #     self._notes.Disable()
        # else:
        #     self.entry = self._command.selected_entry_row.entry
        #     notes = self.entry.notes
        #     self._notes.SetValue(notes)
        
        # Add GUI objects to secondary sizers
        title_box.Add(self._title, 1, wx.EXPAND)
        notes_box.Add(self._notes, 1, wx.EXPAND)
        
        # Add secondary sizers to the main sizer
        self._main_box.Add(title_box, 0, wx.EXPAND | wx.ALL, 5)
        self._main_box.Add(notes_box, 1, wx.EXPAND | wx.ALL, 5)
        
        # Set main sizer to the panel
        self.SetSizer(self._main_box)
        
        # Refresh lauout
        self.Layout()
        
    def _bind_events(self):
        self._notes.Bind(wx.EVT_TEXT, self._on_typing)
        self._notes.Bind(wx.EVT_SET_FOCUS, self._on_set_focus)
    
    def _on_set_focus(self, evet) -> None:
        # self._right_panel.undo_availbale(True)
        ...
        
    def _on_typing(self, event):
        # value = self._notes.GetValue()
        # self.entry.notes = value
        # if not self.undo_in_progress:
        #     self._right_panel.make_snapshot()
        ...
        
    def set_value(self, value: str) -> None:
        self._notes.SetValue(value)
        self._notes.SetInsertionPointEnd()
        
    
    def applay_color_theme(self, theme_name: str):
        self._current_theme = theme_name
        self._text_colour = self._color_themes[self._current_theme]['text']
        self._input_background_colour = self._color_themes[self._current_theme]['input_background']
        
        self._title.SetForegroundColour(self._text_colour)
        self._notes.SetForegroundColour(self._text_colour)
        self._notes.SetBackgroundColour(self._input_background_colour)
        
        self.Refresh()