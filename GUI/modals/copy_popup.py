#!/usr/bin/env python3

import wx 
import ast 


# Starts here iubj oihbnn oihn ;oihn


# class CopyPopup(wx.Frame):
#     def __init__(self, parent: wx.Panel, settings: dict) -> None:
        # self._parent = parent 
        # self._settings = settings

        # self._config = self._settings['copy_popup']
        
#         self._size = ast.literal_eval(self._config['size'])
        
#         super().__init__(None, size=self._size, style=wx.NO_BORDER | wx.STAY_ON_TOP)
        
#         # super().__init__(self._parent, size=self._size)
        
#         # self.SetBackgroundColour(wx.Colour(self._config['frame_background_color']))
        
#         # self.CenterOnScreen()
        
#         self._transparency_timer = wx.Timer(self)
#         self._transparency = int(self._config['current_transparency'])
#         self._transparency_timer.Start(int(self._config['transformation_speed']))
        
#         self._init_ui()
#         self._bind_events()
    
#     def _init_ui(self) -> None:
        
#         main_box = wx.BoxSizer(wx.VERTICAL)
#         message_box = wx.BoxSizer(wx.HORIZONTAL)
        
#         text = wx.StaticText(self, -1, self._config['message'], style=wx.ALIGN_CENTER)
#         font = wx.Font(int(self._config['font_size']), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
#         text.SetForegroundColour(wx.Colour(self._config['text_color']))
#         text.SetFont(font)
        
#         message_box.Add(text, 1, wx.ALIGN_CENTER)
#         main_box.Add(message_box, 1, wx.EXPAND | wx.ALL, 10)
        
#         self.SetSizer(main_box)
#         self.Layout()
        
    
#     def _bind_events(self) -> None:
#         self.Bind(wx.EVT_TIMER, self._on_timer)
#         self.Bind(wx.EVT_PAINT, self._on_paint)
        
#     def _on_paint(self, event) -> None:
#         x, y = self._size
#         dc = wx.PaintDC(self)
#         dc.SetBrush(wx.Brush(self._config['background_color']))
#         dc.SetPen(wx.Pen(self._config['background_color']))
#         dc.DrawRoundedRectangle(0, 0, x, y, int(self._config['round_angle_radius']))
    
#     def _on_timer(self, event) -> None:
#         self._transparency -= int(self._config['transformation_step'])
#         if self._transparency < 0:
#             self.Destroy()
#         self.SetTransparent(self._transparency)
        
        
        
class CopyPopup(wx.Frame):
    def __init__(self, parent: wx.Panel, settings: dict):
        
        self._parent = parent 
        self._settings = settings

        self._config = self._settings['copy_popup']
        self._size = ast.literal_eval(self._config['size'])
        
        super().__init__(self._parent, size=self._size, style=wx.NO_BORDER | wx.STAY_ON_TOP)
        
        self.SetBackgroundColour(wx.Colour(self._config['frame_background_color']))
        
        self.CenterOnScreen()
        
        self._transparency_timer = wx.Timer(self)
        self._transparency = int(self._config['current_transparency'])
        self._transparency_timer.Start(int(self._config['transformation_speed']))
        
        self._init_ui()
        self._bind_events() 
        
    
    def _init_ui(self):
        main_box = wx.BoxSizer(wx.VERTICAL)
        message_box = wx.BoxSizer(wx.HORIZONTAL)
        
        text = wx.StaticText(self, -1, self._config['message'], style=wx.ALIGN_CENTER)
        font = wx.Font(int(self._config['font_size']), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
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
        dc.DrawRoundedRectangle(0, 0, x, y, int(self._config['round_angle_radius']))
    
    def _on_timer(self, event) -> None:
        self._transparency -= int(self._config['transformation_step'])
        if self._transparency <= 0:
            self.Destroy()
        self.SetTransparent(self._transparency)
        
        
        

class CopyApp(wx.App):
    def __init__(self,  parent: wx.Panel, settings: dict):
        super().__init__()
        frame = CopyPopup(parent, settings)
        frame.Show()

def launch_copy_poup(parent: wx.Panel, settings: dict) -> None:
    app = CopyApp(parent, settings)
    app.MainLoop()