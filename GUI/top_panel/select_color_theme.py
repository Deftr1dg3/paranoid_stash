import wx
import ast

from manage_data import ManageData

from GUI.base_panel import BasePanel

# class SelectColorThemePanel(BasePanel):
#     def __init__(self, parent: wx.Panel, manage_data: ManageData, settings: dict, color_themes: dict, theme_name: str) -> None:
#         self._parent = parent 
#         self._manage_data = manage_data
#         self._settings = settings
#         self.color_themes = color_themes
#         self.theme_name = theme_name
        
#         self._size = ast.literal_eval(self._settings['top_panel']['top_right_panel']['size'])
#         self._panel_title = self._settings['top_panel']['top_right_panel']['top_right_panel_title']
#         self._theme_button_label = self._settings['top_panel']['top_right_panel']['theme_button_label']
        
#         self._foreground_color = wx.Colour(self.color_themes[self.theme_name]['text'])
        
#         super().__init__(parent, size=self._size)
        
#         self._init_ui()
#         self._bind_events()
        
#         self.applay_color_theme(self.theme_name)
        
        
class SelectColorThemeFrame(wx.Frame):
    def __init__(self, parent: wx.Panel, settings: dict, color_themes: dict, current_theme: str):
        self._parent = parent 
        self._settings = settings
        self.color_themes = color_themes
        self.current_theme = current_theme
        
        self._size = ast.literal_eval(self._settings['select_color']['size'])
        self._title = self._settings['select_color']['title']
        self._background_color = self._settings['select_color']['background_color']
        self._circle_panel_pen_color = self._settings['select_color']['circle_panel_pen_color']
        self._circle_panel_pen_size = int(self._settings['select_color']['circle_panel_pen_size'])
        
        super().__init__(self._parent, title=self._title, size=self._size)
        
        self.SetBackgroundColour(self._background_color)
        
        self._available_colours = self.color_themes.keys()
        self._radio_buttons = {}
        
        
        
        self._init_ui()
        self._bind_events()
        
    def _init_ui(self):
        ... 
        
    def _bind_events(self):
        ...