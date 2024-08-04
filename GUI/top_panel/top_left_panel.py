#!/usr/bin/env python3

import wx

from GUI.base_panel import BasePanel
# from GUI.menu_functions.menu_functions import MenuFunctions


class TopLeftPanel(BasePanel):
    def __init__(self, parent: BasePanel) -> None:

        self._size = self._settings['top_panel']['top_left_panel']['size']
        self._new_category_label = self._settings['top_panel']['top_left_panel']['new_category_label']
        self._button_size = self._settings['top_panel']['top_left_panel']['new_category_button_size']
        
        self._foreground_color = wx.Colour(self._color_themes[self._current_theme]['text'])
        
        # self._functions = MenuFunctions(self)
        
        super().__init__(parent, size=self._size)
        
        self._init_ui()
        self._bind_events()
        
        self.applay_color_theme()
        
    def _init_ui(self) -> None:
        main_box = wx.BoxSizer(wx.HORIZONTAL) 
        
        main_box.AddStretchSpacer()
        
        self._new_category = wx.Button(self, label=self._new_category_label)

        main_box.Add(self._new_category, 0, wx.ALIGN_CENTRE)
        
        main_box.AddStretchSpacer()
        
        self.SetSizer(main_box)
        self.Layout()
        
    def _bind_events(self) -> None:
        self._new_category.Bind(wx.EVT_BUTTON, self.add_category)
        
    def add_category(self, event) -> None:
        self._functions.add_category()

    def applay_color_theme(self) -> None:
        self.SetBackgroundColour(wx.Colour(self._color_themes[self._current_theme]['medium']))
        self.Refresh()
        