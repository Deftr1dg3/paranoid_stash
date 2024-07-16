import os 
import sys 
sys.path.append(os.getcwd())

import wx

from manage_data import ManageData

from GUI.base_panel import BasePanel
from GUI.body_panel import BodyPanel
from GUI.top_panel import TopPanel


class MainPanel(BasePanel):
    def __init__(self, parent: wx.Frame, manage_date: ManageData, settings: dict, color_themes: dict, theme_name: str) -> None:
        super().__init__(parent)
        self._parent = parent 
        self._manage_data = manage_date
        self._settings = settings
        self.color_themes = color_themes
        self.theme_name = theme_name
        
        self.applay_color_theme(self.theme_name)
        self._init_ui()
    
    def _init_ui(self):
        main_box = wx.BoxSizer(wx.VERTICAL)
        top_bar_box = wx.BoxSizer(wx.HORIZONTAL)
        body_box = wx.BoxSizer(wx.HORIZONTAL)
        
        self._top_panel = TopPanel(self, self._manage_data, self._settings, self.color_themes, self.theme_name)
        self._body_panel = BodyPanel(self, self._manage_data, self._settings, self.color_themes, self.theme_name)
        
        top_bar_box.Add(self._top_panel, 1, wx.EXPAND)
        body_box.Add(self._body_panel, 1, wx.EXPAND)
        
        main_box.Add(top_bar_box, 0, wx.EXPAND)
        main_box.Add(body_box, 1, wx.EXPAND | wx.TOP, 0)
        
        self.SetSizer(main_box)
        self.Layout()
        
    def applay_color_theme(self, theme_name: str):
        self.theme_name = theme_name
        self.SetBackgroundColour(wx.Colour(self.color_themes[theme_name]['dark']))
        self.Refresh()
           