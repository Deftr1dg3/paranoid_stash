from __future__ import annotations
import wx

from GUI.base_panel import BasePanel
from GUI.left_panel.left_panel import LeftPanel
from GUI.right_panel.right_panel import RightPanel
from GUI.mid_panel.mid_panel import MidPanel

class BodyPanel(BasePanel):
    def __init__(self, parent: BasePanel) -> None:
        super().__init__(parent)
                                
        self._init_ui()
        self.applay_color_theme()
        
        BasePanel.set_body_panel(self)
    
    def _init_ui(self):
        main_box = wx.BoxSizer(wx.HORIZONTAL)
        left_box = wx.BoxSizer(wx.VERTICAL)
        mid_box = wx.BoxSizer(wx.VERTICAL)
        right_box = wx.BoxSizer(wx.VERTICAL)
        
        self._left_panel = LeftPanel(self)
        self._mid_panel = MidPanel(self)
        self._right_panel = RightPanel(self)
        
        left_box.Add(self._left_panel, 1, wx.EXPAND | wx.TOP, 1)
        mid_box.Add(self._mid_panel, 1, wx.EXPAND)
        right_box.Add(self._right_panel, 1, wx.EXPAND | wx.TOP, 1)
        
        main_box.Add(left_box, 0, wx.EXPAND)
        main_box.Add(mid_box, 1, wx.EXPAND)
        main_box.Add(right_box, 0, wx.EXPAND)
        
        self.SetSizer(main_box)
        self.Layout()
    
    @property
    def left_panel(self):
        return self._left_panel

    @property
    def mid_panel(self):
        return self._mid_panel

    @property
    def right_panel(self):
        return self._right_panel
        
    def applay_color_theme(self):
        self.SetBackgroundColour(wx.Colour(self._color_themes[self._current_theme]['dark']))
        self.Refresh()
        
        