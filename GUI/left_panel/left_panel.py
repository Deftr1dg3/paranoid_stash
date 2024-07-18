import sys 
import os 
sys.path.append(os.getcwd())

import wx
import ast

from manage_data import ManageData, DataFile
from manage_data import GeneratePassword, ValidatePassword, PasswordStrength

from GUI.base_panel import BasePanel
from GUI.left_panel.category_row import CategoryRow

class LeftPanel(BasePanel):
    def __init__(self, parent: wx.Panel, manage_date: ManageData, settings: dict, color_themes: dict, current_theme: str) -> None:
        self._parent = parent 
        self._manage_data = manage_date
        self._settings = settings
        self._color_themes = color_themes
        self._current_theme = current_theme
        
        self._panel_size = ast.literal_eval(self._settings['left_panel']['size'])
        self._scroll_settings = ast.literal_eval(self._settings['left_panel']['scroll_settings'])
        
        super().__init__(self._parent, size=self._panel_size)
        
        self._init_ui()
        
        self.applay_color_theme(self._current_theme)
        
    def _init_ui(self):
        main_box = wx.BoxSizer(wx.VERTICAL)
        
        # Create ScrolledWindow
        self.scroll = wx.ScrolledWindow(self, -1)
        self.scroll.SetScrollbars(*self._scroll_settings)
        
        # Create secondary sizer for ScrolledWindow
        scroll_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Create GUI objects
        for category in self._manage_data.all_categories():
            self._display_category(self.scroll, scroll_sizer, category) 
        
        # Rest category rows dict 
        self._category_rows = {}
        
        # Add sizer to ScrolledWindow
        self.scroll.SetSizer(scroll_sizer)
        
        # Add scroll window to the main sizer
        main_box.Add(self.scroll, 1, wx.EXPAND)
        
        # Set main sizer to the panel
        self.SetSizer(main_box)
        
        # Refresh layout
        self.Layout()
    
    def _display_category(self, scroll, scroll_sizer, category_name: str) -> None:
        category_row = CategoryRow(scroll, self._manage_data, self._settings, self._color_themes, self._current_theme, category_name)
        # self._category_rows[category.id] = category_row
        scroll_sizer.Add(category_row, 0, wx.EXPAND)
        
    def applay_color_theme(self, theme_name: str):
        self.theme_name = theme_name
        self.SetBackgroundColour(wx.Colour(self._color_themes[theme_name]['medium']))
        self.Refresh()
        
        