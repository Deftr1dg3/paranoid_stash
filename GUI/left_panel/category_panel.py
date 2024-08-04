#!/usr/bin/env python3


import wx

from GUI.base_panel import BasePanel
from manage_data import ManageData

class CategoryNamePanel(BasePanel):
    def __init__(self, parent: BasePanel, category_name: str) -> None:
        self._parent = parent 
        
        self._category_max_len = self._settings['left_panel']['category_max_len']
        self._replacement_characters = self._settings['left_panel']['replacement_characters']
        
        self._size = self._settings['left_panel']['category_panel_size']
        self._name = self._format_category_name(category_name)

        super().__init__(self._parent, size=self._size)
        
        self._text_colour = self._color_themes[self._current_theme]['text']
        
        # Initializing visible objects
        self._init_ui()
        self.applay_color_theme()
        
    def _init_ui(self) -> None:
        """ Function initializing visible interface. """
        
        # Create main sizer
        main_box = wx.BoxSizer(wx.HORIZONTAL)
        
        # Create gui object
        self._category_name = wx.StaticText(self, label=self._name)
        
        # Add gui object to the main sizer
        main_box.Add(self._category_name, 0, wx.TOP | wx.LEFT, 6)
        
        # Set main sizer to the panel
        self.SetSizer(main_box)
        
        # Refresh lauout
        self.Layout()
        
    def _format_category_name(self, category_name: str) -> str:
        if len(category_name) > self._category_max_len:
            category_name = category_name[:self._category_max_len] + self._replacement_characters
        return category_name
    
    def set_text_colour(self, colour: wx.Colour) -> None:
        self._category_name.SetForegroundColour(colour)
        self.Refresh() 
        
    def applay_color_theme(self):
        self._text_colour = self._color_themes[self._current_theme]['text']
        self.SetBackgroundColour(self._color_themes[self._current_theme]['medium'])
        self.Refresh() 