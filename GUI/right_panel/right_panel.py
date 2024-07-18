#!/usr/bin/env python3


import wx 
import ast

from GUI.right_panel.edit_panel import EditPanel
from GUI.right_panel.notes_panel import NotesPanel
from manage_data import ManageData
from GUI.base_panel import BasePanel

class RightPanel(BasePanel):
    def __init__(self, parent: wx.Panel, manage_date: ManageData, settings: dict, color_themes: dict, current_theme: str) -> None:
        self._parent = parent 
        self._manage_data = manage_date
        self._settings = settings
        self._color_themes = color_themes
        self._current_theme = current_theme
        
        self._size = ast.literal_eval(self._settings['right_panel']['size'])
        
        super().__init__(self._parent, size=self._size)
    
        self._init_ui()
        self.applay_color_theme(self._current_theme)
        

    def _init_ui(self):
        """ Function initializing visible interface. """
        
        # Create main sizer
        self._main_box = wx.BoxSizer(wx.VERTICAL)
        
        # Create secondary sizers
        edit_box = wx.BoxSizer(wx.HORIZONTAL)
        notes_box = wx.BoxSizer(wx.HORIZONTAL)
        
        # Create GUI objects
        self._edit_panel = EditPanel(self, self._manage_data, self._settings, self._color_themes, self._current_theme)
        self._notes_panel = NotesPanel(self, self._manage_data, self._settings, self._color_themes, self._current_theme)
        
        edit_box.Add(self._edit_panel, 1, wx.EXPAND)
        notes_box.Add(self._notes_panel, 1, wx.EXPAND)
        
        self._main_box.Add(edit_box, 1, wx.EXPAND)
        self._main_box.Add(notes_box, 0, wx.EXPAND)
        
        self.SetSizer(self._main_box)
        self.Layout()
        
    def refresh(self):
        self._main_box.Clear(True)
        self._init_ui()
        
    def applay_color_theme(self, theme_name: str):
        self._current_theme = theme_name
        self.SetBackgroundColour(wx.Colour(self._color_themes[theme_name]['medium']))
        self.Refresh()