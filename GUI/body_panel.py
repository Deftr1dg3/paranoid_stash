import wx
from itertools import cycle

from manage_data import ManageData
from GUI.base_panel import BasePanel
from GUI.left_panel.left_panel import LeftPanel
from GUI.right_panel.right_panel import RightPanel


class BodyPanel(BasePanel):
    def __init__(self, parent: wx.Panel, manage_date: ManageData, settings: dict, color_themes: dict, current_theme: str) -> None:
        super().__init__(parent)
        self._parent = parent 
        self._manage_data = manage_date
        self._settings = settings
        self._color_themes = color_themes
        self._current_theme = current_theme
        
        self._init_ui()
        self.applay_color_theme(self._current_theme)
        
        self._body_panel = self
    
    def _init_ui(self):
        main_box = wx.BoxSizer(wx.HORIZONTAL)
        left_box = wx.BoxSizer(wx.VERTICAL)
        mid_box = wx.BoxSizer(wx.VERTICAL)
        right_box = wx.BoxSizer(wx.VERTICAL)
        
        
        self._left_panel = LeftPanel(self, self._manage_data, self._settings, self._color_themes, self._current_theme)
        
        self._right_panel = RightPanel(self, self._manage_data, self._settings, self._color_themes, self._current_theme)
        
        
    
        left_box.Add(self._left_panel, 1, wx.EXPAND | wx.TOP, 1)
        
        right_box.Add(self._right_panel, 1, wx.EXPAND | wx.TOP, 1)
        
        
        
        main_box.Add(left_box, 0, wx.EXPAND)
        
        main_box.Add(right_box, 0, wx.EXPAND)
        
        
        
        self.SetSizer(main_box)
        self.Layout()
        
    def applay_color_theme(self, theme_name: str):
        self._current_theme = theme_name
        self.SetBackgroundColour(wx.Colour(self._color_themes[theme_name]['dark']))
        self.Refresh()
        
        