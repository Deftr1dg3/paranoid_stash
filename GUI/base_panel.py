from __future__ import annotations
import wx
import json


# SETTINGS_PATH = './GUI/gui_settings.json'
# COLOR_THEMES_PATH = './GUI/color_themes.json'

# with open(SETTINGS_PATH, 'r') as f:
#     SETTINGS = json.load(f)

# with open(COLOR_THEMES_PATH, 'r') as f:
#     COLOR_THEMES: dict = json.load(f)

class BasePanel(wx.Panel):
    _instances = []
    category_rows = []
    entry_rows = []
    
    body = None
    top_panel = None
    
    def __new__(cls, *args, **kwargs):
        i = super().__new__(cls, *args, **kwargs)
        cls._instances.append(i)
        return i

    @classmethod
    def set_body_panel(cls, inst: BasePanel):
        cls.body = inst
        
    @classmethod
    def set_top_panel(cls, inst: BasePanel):
        cls.top_panel = inst

        
    def applay_color_theme(self, theme_name: str):
        raise NotImplementedError

