import wx

from manage_data import ManageData

from GUI.base_panel import BasePanel
from GUI.body_panel import BodyPanel
from GUI.top_panel import TopPanel
from GUI.menu_functions.menu_functions import MenuFunctions

class MainPanel(BasePanel):
    def __init__(self, parent: wx.Frame, manage_date: ManageData, settings: dict, color_themes: dict, current_theme: str) -> None:
        super().__init__(parent)
        
        BasePanel.set_manage_data(manage_date)
        BasePanel.set_settings(settings)
        BasePanel.set_color_themes(color_themes)
        BasePanel.set_current_theme(current_theme)
        BasePanel.set_menu_fucntions(MenuFunctions(self))
        

        self._init_ui()
        self.applay_color_theme()
    
    def _init_ui(self):
        main_box = wx.BoxSizer(wx.VERTICAL)
        top_bar_box = wx.BoxSizer(wx.HORIZONTAL)
        body_box = wx.BoxSizer(wx.HORIZONTAL)
        
        self._top_panel = TopPanel(self)
        self._body_panel = BodyPanel(self)
        
        top_bar_box.Add(self._top_panel, 1, wx.EXPAND)
        body_box.Add(self._body_panel, 1, wx.EXPAND)
        
        main_box.Add(top_bar_box, 0, wx.EXPAND)
        main_box.Add(body_box, 1, wx.EXPAND | wx.TOP, 0)
        
        self.SetSizer(main_box)
        self.Layout()
        
    def applay_color_theme(self):
        self.SetBackgroundColour(wx.Colour(self._color_themes[self._current_theme]['dark']))
        self.Refresh()
           