#!/usr/bin/env python3

import wx 

from GUI.base_panel import BasePanel

        
class CopyPopup(wx.Frame):
    def __init__(self, parent: BasePanel):
        
        self._parent = parent 
        self._settings = parent.settings

        self._config = self._settings['copy_popup']
        self._size = self._config['size']
        
        super().__init__(None, size=self._size, style=wx.NO_BORDER | wx.STAY_ON_TOP)
        
        self.SetBackgroundColour(wx.Colour(self._config['frame_background_color']))
        
        self.CenterOnScreen()
        
        self._transparency_timer = wx.Timer(self)
        self._transparency = self._config['current_transparency']
        self._transparency_timer.Start(self._config['transformation_speed'])
        
        self._init_ui()
        self._bind_events() 
        
    
    def _init_ui(self):
        main_box = wx.BoxSizer(wx.VERTICAL)
        message_box = wx.BoxSizer(wx.HORIZONTAL)
        
        text = wx.StaticText(self, -1, self._config['message'], style=wx.ALIGN_CENTER)
        font = wx.Font(self._config['font_size'], wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        text.SetForegroundColour(wx.Colour(self._config['text_color']))
        text.SetFont(font)
        
        message_box.Add(text, 1, wx.ALIGN_CENTER)
        main_box.Add(message_box, 1, wx.EXPAND | wx.ALL, 10)
        
        self.SetSizer(main_box)
        self.Layout()
        
    
    def _bind_events(self):
        self.Bind(wx.EVT_TIMER, self._on_timer)
        self.Bind(wx.EVT_PAINT, self._on_paint)
        
    def _on_paint(self, event) -> None:
        x, y = self._size
        dc = wx.PaintDC(self)
        dc.SetBrush(wx.Brush(self._config['background_color']))
        dc.SetPen(wx.Pen(self._config['background_color']))
        dc.DrawRoundedRectangle(0, 0, x, y, self._config['round_angle_radius'])
    
    def _on_timer(self, event) -> None:
        self._transparency -= self._config['transformation_step']
        if self._transparency <= 0:
            self.Destroy()
        self.SetTransparent(self._transparency)
        