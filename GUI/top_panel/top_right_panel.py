import wx
import ast

from manage_data import ManageData

from GUI.base_panel import BasePanel
from GUI.top_panel.select_color_theme import SelectColorThemeFrame, launch_select_color

class TopRightPanel(BasePanel):
    def __init__(self, parent: wx.Panel, manage_date: ManageData, settings: dict, color_themes: dict, current_theme: str) -> None:
        self._parent = parent 
        self._manage_data = manage_date
        self._settings = settings
        self._color_themes = color_themes
        self._current_theme = current_theme
        
        self._size = ast.literal_eval(self._settings['top_panel']['top_right_panel']['size'])
        self._panel_title = self._settings['top_panel']['top_right_panel']['top_right_panel_title']
        self._theme_button_label = self._settings['top_panel']['top_right_panel']['theme_button_label']
        
        self._foreground_color = wx.Colour(self._color_themes[self._current_theme]['text'])
        
        super().__init__(parent, size=self._size)
        
        self._init_ui()
        self.applay_color_theme(self._current_theme)
        
        self._bind_events()
        
    
    def _init_ui(self):
        main_box = wx.BoxSizer(wx.HORIZONTAL)
        title_box = wx.BoxSizer(wx.VERTICAL)
        button_box = wx.BoxSizer(wx.VERTICAL)
        
        # Create gui objects
        self._entry_edit_title = wx.StaticText(self, label=self._panel_title)
        self._theme_button = wx.Button(self, label=self._theme_button_label)
        # self._theme_button = wx.StaticText(self, label=self._theme_button_label)
        
        # Add created objects to the sizers
        title_box.Add(self._entry_edit_title, 0, wx.TOP | wx.LEFT, 7)
        button_box.Add(self._theme_button, 0, wx.TOP | wx.RIGHT, 5)
        
        # Add sizers to the main sizer.
        main_box.Add(title_box, 0, wx.EXPAND)
        main_box.AddStretchSpacer()
        main_box.Add(button_box, 0, wx.EXPAND)
        
        # Set main sizer to the panel
        self.SetSizer(main_box)
        self.Layout()
        
    def _bind_events(self):
        self._theme_button.Bind(wx.EVT_BUTTON, self._on_color_theme)
    
    def _on_color_theme(self, event):
        launch_select_color(self, self._settings, self._color_themes, self._current_theme)
        
    def applay_color_theme(self, theme_name: str):
        self._current_theme = theme_name
        self.SetBackgroundColour(wx.Colour(self._color_themes[self._current_theme]['medium']))
        # self.SetBackgroundColour('red')
        # Foreground color works only woth Static Text ----------------------------------------
        self._entry_edit_title.SetForegroundColour(wx.Colour(self._color_themes[self._current_theme]['text']))
        self._theme_button.SetForegroundColour(wx.Colour(self._color_themes[self._current_theme]['text']))
        self.Refresh()
        
        