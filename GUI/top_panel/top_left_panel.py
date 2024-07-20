#!/usr/bin/env python3

import sys 
import os 
sys.path.append(os.getcwd())

import wx
import random
import ast
from itertools import cycle

from manage_data import ManageData, DataFile
from manage_data import GeneratePassword, ValidatePassword, PasswordStrength

from GUI.base_panel import BasePanel

class TopLeftPanel(BasePanel):
    def __init__(self, parent: wx.Panel, manage_date: ManageData, settings: dict, color_themes: dict, theme_name: str) -> None:
        self._parent = parent 
        self._manage_data = manage_date
        self._settings = settings
        self._color_themes = color_themes
        self._current_theme = theme_name
        
        self._size = ast.literal_eval(self._settings['top_panel']['top_left_panel']['size'])
        self._new_category_label = self._settings['top_panel']['top_left_panel']['new_category_label']
        self._button_size = ast.literal_eval(self._settings['top_panel']['top_left_panel']['new_category_button_size'])
        
        self._foreground_color = wx.Colour(self._color_themes[self._current_theme]['text'])
        
        super().__init__(parent, size=self._size)
        
        self._init_ui()
        self._bind_events()
        
        self.applay_color_theme(self._current_theme)
        
        self._g = self._num_gen()
        
        
    def _init_ui(self):
        main_box = wx.BoxSizer(wx.HORIZONTAL) 
        
        main_box.AddStretchSpacer()
        
        self._new_category = wx.Button(self, label=self._new_category_label)
        # self._new_category = wx.StaticText(self, label=self._new_category_label)

        main_box.Add(self._new_category, 0, wx.ALIGN_CENTRE)
        
        main_box.AddStretchSpacer()
        
        self.SetSizer(main_box)
        self.Layout()
        
    def _bind_events(self):
        self._new_category.Bind(wx.EVT_BUTTON, self._add_category)
        
    def _num_gen(self):
        n = 1
        while True:
            yield n
            n += 1
        
    def _add_category(self, event):
        self._manage_data.add_category(f"New{next(self._g)}")
        self._manage_data.selected_entry = None
        self._manage_data.search_results = None
        self.body.left_panel.refresh() # type: ignore
        self.body.mid_panel.refresh() # type: ignore
        self.body.right_panel.refresh() # type: ignore
        
    def applay_color_theme(self, theme_name: str):
        self._current_theme = theme_name
        self.SetBackgroundColour(wx.Colour(self._color_themes[self._current_theme]['medium']))
        # self.SetBackgroundColour('red')
        # Foreground color works only woth Static Text ----------------------------------------
        # self._new_category.SetForegroundColour(wx.Colour(self.color_themes[self.theme_name]['text']))
        self.Refresh()