#!/usr/bin/env python3

import wx 

from GUI.right_panel.edit_panel import EditPanel
from GUI.right_panel.notes_panel import NotesPanel
from GUI.base_panel import BasePanel

class RightPanel(BasePanel):
    def __init__(self, parent: BasePanel) -> None:
        self._parent = parent 
        
        self._size = self._settings['right_panel']['size']
        
        super().__init__(self._parent, size=self._size)
    
        self._init_ui()
        self.applay_color_theme()
        
    def _init_ui(self):
        """ Function initializing visible interface. """
        
        # Create main sizer
        self._main_box = wx.BoxSizer(wx.VERTICAL)
        
        # Create secondary sizers
        edit_box = wx.BoxSizer(wx.HORIZONTAL)
        notes_box = wx.BoxSizer(wx.HORIZONTAL)
        
        # Create GUI objects
        self._edit_panel = EditPanel(self)
        self._notes_panel = NotesPanel(self)
        
        edit_box.Add(self._edit_panel, 1, wx.EXPAND)
        notes_box.Add(self._notes_panel, 1, wx.EXPAND)
        
        self._main_box.Add(edit_box, 1, wx.EXPAND)
        self._main_box.Add(notes_box, 0, wx.EXPAND)
        
        self._dummy_panel = wx.Panel(self, size=(0, 0))
        
        self.SetSizer(self._main_box)
        self.Layout()
        
    def refresh(self):
        self._main_box.Clear(True)
        self._init_ui()
    
    def deselect_all(self):
        self._dummy_panel.SetFocus()
        
    def applay_color_theme(self):
        self.SetBackgroundColour(wx.Colour(self._color_themes[self._current_theme]['medium']))
        self.Refresh()