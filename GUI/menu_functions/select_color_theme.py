from __future__ import annotations
import wx
import ast
import json

from GUI.base_panel import BasePanel

class CirclePanel(BasePanel):
    def __init__(self, parent: BasePanel, theme: str):
        super().__init__(parent)
        
        self._theme = theme
        
        self._brush_color = self._color_themes[self._theme]['dark']
        self._pen_colour = self._color_themes[self._theme]['medium']
        self._pen_size = int(self._settings['select_color']['circle_panel_pen_size'])
        
        self._bind_events()
        self.applay_color_theme()
        
    
    def _bind_events(self) -> None:
        self.Bind(wx.EVT_PAINT, self._on_paint)

    def _on_paint(self, event) -> None:
        dc = wx.PaintDC(self)
        dc.Clear()
        w, h = self.GetSize()
        dc.SetPen(wx.Pen(self._pen_colour, self._pen_size))
        dc.SetBrush(wx.Brush(self._brush_color))
        radius = min(w, h) // 2 - 2
        dc.DrawCircle(w // 2, h // 2, radius - self._pen_size)
        
    def applay_color_theme(self):
        self.SetBackgroundColour(wx.Colour(self._color_themes[self._current_theme]['dark']))
        self.Refresh()


class SelectColorThemePanel(BasePanel):
    def __init__(self, parent: wx.Frame) -> None:
        super().__init__(parent)
        self._parent = parent 
        
        self._settings_path = self._settings['global']['settings_path']
        self._size = ast.literal_eval(self._settings['select_color']['size'])
        
        self._radio_buttons = {}
        
        self._init_ui()
        
        self.applay_color_theme()
        
        self.top_panel.top_mid_panel.deselect_search() 
        
    def _init_ui(self):
        main_box = wx.BoxSizer(wx.VERTICAL)
        
        thems_row_box = wx.BoxSizer(wx.HORIZONTAL)
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        
        for theme in self._color_themes.keys():
            theme_box = wx.BoxSizer(wx.VERTICAL)
            
            circle = CirclePanel(self, theme)
            
            radio_button = wx.RadioButton(self)
            self._radio_buttons[radio_button.GetId()] = theme
            if theme == self._current_theme:
                radio_button.SetValue(True)
                
            radio_button_box = wx.BoxSizer(wx.HORIZONTAL)  # New box sizer for centering radio buttons
            radio_button_box.AddStretchSpacer()
            radio_button_box.Add(radio_button, 0, wx.ALL, 5)
            radio_button_box.AddStretchSpacer()
            radio_button.Bind(wx.EVT_RADIOBUTTON, self._on_radio_button)
            
            theme_box.Add(circle, 1, wx.EXPAND | wx.ALL, 1)
            theme_box.Add(radio_button_box, 0, wx.EXPAND | wx.BOTTOM, 10)
            
            thems_row_box.Add(theme_box, 1, wx.EXPAND)
        
        button_box.AddStretchSpacer()
        
        main_box.Add(thems_row_box, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        main_box.Add(button_box, 0, wx.EXPAND | wx.BOTTOM, 10)
        
        self.SetSizer(main_box)
        self.Layout()
    
    def _save_updated_color_theme(self):
        with open(self._settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        settings.update({'color_theme': self._current_theme})
        with open(self._settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2)
            
    def _on_radio_button(self, event):
        radio_button = event.GetEventObject()
        theme = self._radio_buttons[radio_button.GetId()]
        BasePanel.set_current_theme(theme)
        for _ in range(len(self.instances)):
            try:
                instance = self.instances.popleft()
                instance.applay_color_theme()
            except Exception as ex:
                pass
            else:
                self.instances.append(instance)
        self._save_updated_color_theme()
    
    def applay_color_theme(self):
        self.SetBackgroundColour(wx.Colour(self._color_themes[self._current_theme]['dark']))
        self.Refresh()
        
        
class SelectColorThemeFrame(wx.Frame):
    
    def __init__(self, parent: BasePanel, settings: dict, color_themes: dict):
        
        self._parent = parent 
        self._settings = settings
        self._color_themes = color_themes
        
        self._size = ast.literal_eval(self._settings['select_color']['size'])
        self._title = self._settings['select_color']['title']
        
        x = len(self._color_themes) * 70 
        y = self._size[1]
        
        super().__init__(self._parent, title=self._title, size=(x, y), style=wx.CLOSE_BOX)
        
        self.SetMinSize((x, y))
        self.SetMaxSize((x, y))
        
        self._init_ui()
        
    def _init_ui(self):
        panel = SelectColorThemePanel(self) 

