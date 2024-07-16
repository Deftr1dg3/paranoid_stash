import wx
from itertools import cycle

from manage_data import ManageData

from GUI.base_panel import BasePanel
from GUI.left_panel.left_panel import LeftPanel


class BodyPanel(BasePanel):
    def __init__(self, parent: wx.Panel, manage_date: ManageData, settings: dict, color_themes: dict, theme_name: str) -> None:
        super().__init__(parent)
        self._parent = parent 
        self._manage_data = manage_date
        self._settings = settings
        self.color_themes = color_themes
        self.theme_name = theme_name
        
        self.applay_color_theme(self.theme_name)
        self._init_ui()
        
        self.ind = iter(cycle(color_themes.keys()))
    
    def _init_ui(self):
        main_box = wx.BoxSizer(wx.HORIZONTAL)
        left_box = wx.BoxSizer(wx.VERTICAL)
        mid_box = wx.BoxSizer(wx.VERTICAL)
        right_box = wx.BoxSizer(wx.VERTICAL)
        
        self._left_panel = LeftPanel(self, self._manage_data, self._settings, self.color_themes, self.theme_name)
    
    
        left_box.Add(self._left_panel, 1, wx.EXPAND | wx.TOP, 1)
        
        
        main_box.Add(left_box, 0, wx.EXPAND)
        
        self.SetSizer(main_box)
        self.Layout()
        
        b = wx.Button(self, label='Click me')
        
        b.Bind(wx.EVT_BUTTON, self.on_button)
    
    def on_button(self, event):
        n = next(self.ind)
        for instance in self._instances:
            instance.applay_color_theme(n)
        
    def applay_color_theme(self, theme_name: str):
        self.theme_name = theme_name
        self.SetBackgroundColour(wx.Colour(self.color_themes[theme_name]['dark']))
        self.Refresh()
        
        