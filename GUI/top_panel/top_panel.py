
import wx

from GUI.base_panel import BasePanel
from GUI.top_panel.top_left_panel import TopLeftPanel
from GUI.top_panel.top_mid_panel import TopMidPanel
from GUI.top_panel.top_right_panel import TopRightPanel


class TopPanel(BasePanel):
    def __init__(self, parent: BasePanel) -> None:
        super().__init__(parent, size=(-1, 30))

        self._init_ui()
        self.applay_color_theme()
        
        BasePanel.set_top_panel(self)
        
    def _init_ui(self):
        main_box = wx.BoxSizer(wx.HORIZONTAL)
        left_box = wx.BoxSizer(wx.VERTICAL)
        mid_box = wx.BoxSizer(wx.VERTICAL)
        right_box = wx.BoxSizer(wx.VERTICAL)
        
        self._top_left_panel = TopLeftPanel(self)
        self._top_mid_panel = TopMidPanel(self)
        self._top_right_panel = TopRightPanel(self)
        
        left_box.Add(self._top_left_panel, 1, wx.EXPAND)
        mid_box.Add(self._top_mid_panel, 1, wx.EXPAND)
        right_box.Add(self._top_right_panel, 1, wx.EXPAND)
        
        main_box.Add(left_box, 0 , wx.EXPAND)
        main_box.Add(mid_box, 1 , wx.EXPAND)
        main_box.Add(right_box, 0 , wx.EXPAND)
        
        self.SetSizer(main_box)
        self.Layout()
    
    @property
    def top_left_panel(self):
        return self._top_left_panel
    
    @property
    def top_mid_panel(self):
        return self._top_mid_panel
    
    @property
    def top_right_panel(self):
        return self._top_right_panel
        
    def applay_color_theme(self):
        self.SetBackgroundColour(wx.Colour(self._color_themes[self._current_theme]['medium']))
        self.Refresh()
        