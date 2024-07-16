import os 
import sys 

import wx

from manage_data import ManageData

from GUI.base_panel import BasePanel
from GUI.top_panel.top_left_panel import TopLeftPanel
from GUI.top_panel.top_mid_panel import TopMidPanel
from GUI.top_panel.top_right_panel import TopRightPanel


class TopPanel(BasePanel):
    def __init__(self, parent: wx.Panel, manage_date: ManageData, settings: dict, color_themes: dict, theme_name: str) -> None:
        super().__init__(parent, size=(-1, 30))
        self._parent = parent 
        self._manage_data = manage_date
        self._settings = settings
        self.color_themes = color_themes
        self.theme_name = theme_name
        
        self.applay_color_theme(self.theme_name)
        self._init_ui()
        
    def _init_ui(self):
        main_box = wx.BoxSizer(wx.HORIZONTAL)
        left_box = wx.BoxSizer(wx.VERTICAL)
        mid_box = wx.BoxSizer(wx.VERTICAL)
        right_box = wx.BoxSizer(wx.VERTICAL)
        
        top_left_panel = TopLeftPanel(self, self._manage_data, self._settings, self.color_themes, self.theme_name)
        top_mid_panel = TopMidPanel(self, self._manage_data, self._settings, self.color_themes, self.theme_name)
        top_right_panel = TopRightPanel(self, self._manage_data, self._settings, self.color_themes, self.theme_name)
        
        left_box.Add(top_left_panel, 1, wx.EXPAND)
        mid_box.Add(top_mid_panel, 1, wx.EXPAND)
        right_box.Add(top_right_panel, 1, wx.EXPAND)
        
        main_box.Add(left_box, 0 , wx.EXPAND)
        main_box.Add(mid_box, 1 , wx.EXPAND)
        main_box.Add(right_box, 0 , wx.EXPAND)
        
        self.SetSizer(main_box)
        self.Layout()
        
    def applay_color_theme(self, theme_name: str):
        self.theme_name = theme_name
        self.SetBackgroundColour(wx.Colour(self.color_themes[theme_name]['medium']))
        self.Refresh()
        