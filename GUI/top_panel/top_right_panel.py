import wx
import ast

from GUI.base_panel import BasePanel
from GUI.menu_functions.menu_functions import MenuFunctions

class TopRightPanel(BasePanel):
    def __init__(self, parent: BasePanel) -> None:
        
        self._size = ast.literal_eval(self._settings['top_panel']['top_right_panel']['size'])
        self._panel_title = self._settings['top_panel']['top_right_panel']['top_right_panel_title']
        self._theme_button_label = self._settings['top_panel']['top_right_panel']['theme_button_label']
        self._color_panel_active = False
        
        super().__init__(parent, size=self._size)
        
        self._functions = MenuFunctions(self)
        
        self._init_ui()
        self.applay_color_theme()
        
        self._bind_events()
        
    
    def _init_ui(self):
        main_box = wx.BoxSizer(wx.HORIZONTAL)
        title_box = wx.BoxSizer(wx.VERTICAL)
        button_box = wx.BoxSizer(wx.VERTICAL)
        
        # Create gui objects
        self._entry_edit_title = wx.StaticText(self, label=self._panel_title)
        self._theme_button = wx.Button(self, label=self._theme_button_label)
        
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
        self._functions.choose_color_theme()
                
    def applay_color_theme(self):
        self.SetBackgroundColour(wx.Colour(self._color_themes[self._current_theme]['medium']))
        self._entry_edit_title.SetForegroundColour(wx.Colour(self._color_themes[self._current_theme]['text']))
        self._theme_button.SetForegroundColour(wx.Colour(self._color_themes[self._current_theme]['text']))
        self.Refresh()
        
        