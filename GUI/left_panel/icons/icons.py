#!/usr/bin/env python3


import wx
import ast

from GUI.base_panel import BasePanel
from GUI.left_panel.icons.icons_names import IconNames

class IconPanel(BasePanel):
    def __init__(self, parent: BasePanel, icon_name: IconNames) -> None:
        self._parent = parent 
        
        self._icon_name = icon_name
        self._size = ast.literal_eval(self._settings['left_panel']['icon_panel_size'])
        
        super().__init__(self._parent, size=self._size)
        
        self._icon_colour = self._color_themes[self._current_theme]['selection']
        self._pen_colour = self._color_themes[self._current_theme]['medium']
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        self.applay_color_theme()
        
    def _get_icon_function(self):
        match self._icon_name:
            case IconNames.DATABASE:
                return self._database_icon
            case IconNames.FUNDS:
                return self._funds_icon
            case IconNames.PAYMENTS:
                return self._payments_icon
            case IconNames.CRYPTO:
                return self._crypto_icon
            case IconNames.DEVOPS:
                return self._devops_icon
            case IconNames.INTERNET:
                return self._internet_icon
            case IconNames.EMAIL:
                return self._email_icon
            case _:
                return self._folder_icon

    def OnPaint(self, event) -> None:
        icon = self._get_icon_function()
        dc = wx.PaintDC(self)
        icon(dc)
        
    def _folder_icon(self, dc: wx.PaintDC) -> None:
        dc.SetPen(wx.Pen(wx.Colour(self._pen_colour), 1))
        dc.SetBrush(wx.Brush(self._icon_colour))
        dc.DrawRoundedRectangle(9, 6, 10, 10, 2)
        dc.DrawRoundedRectangle(7, 8, 23, 15, 3)
        
    def _email_icon(self,dc: wx.PaintDC) -> None:
        dc.SetPen(wx.Pen(wx.Colour(self._icon_colour), 1))
        dc.SetBrush(wx.Brush('#00000000'))        
        dc.DrawLines(((6, 8), (17, 15), (17, 15), (29, 8)))
        dc.DrawRoundedRectangle(5, 6, 25, 16, 3)
    
    def _internet_icon(self,dc: wx.PaintDC) -> None:
        dc.SetPen(wx.Pen(wx.Colour(self._icon_colour), 1))
        dc.SetBrush(wx.Brush('#00000000'))
        dc.DrawSpline(((15, 5), (19, 9),  (21, 15), (19, 20), (15, 25)))
        dc.DrawSpline(((15, 5), (11, 9),  (9, 15), (11, 20), (15, 25)))
        dc.DrawSpline(((7, 9), (10, 10), (15, 11),   (21, 10), (23, 9)))
        dc.DrawSpline(((5, 13), (9, 15), (15, 16),  (21, 15), (25, 13)))
        dc.DrawSpline(((5, 17), (9, 20), (15, 21),  (21, 20), (25, 17)))
        dc.DrawLine((15, 5), (15, 25))
        dc.DrawCircle(15, 15, 10)
        
    def _devops_icon(self, dc: wx.PaintDC) -> None:
        font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        dc.SetTextForeground(self._icon_colour)
        dc.DrawText(">_", 7, 5)
        
    def _crypto_icon(self, dc: wx.PaintDC) -> None:
        dc.SetPen(wx.Pen(wx.Colour(self._icon_colour), 2))
        dc.SetBrush(wx.Brush(wx.Colour("#00000000")))
        font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        dc.SetTextForeground(self._icon_colour)
        dc.DrawText("B", 9, 7)
        dc.DrawCircle(15, 15, 10)
        
    def _payments_icon(self, dc: wx.PaintDC) -> None:
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen(wx.Colour(self._icon_colour), 1))
        dc.SetBrush(wx.Brush('#00000000'))
        dc.DrawRoundedRectangle(5, 7, 25, 16, 3)
        dc.SetPen(wx.Pen(wx.Colour('#00000000'), 1))
        dc.SetBrush(wx.Brush(self._icon_colour))
        dc.DrawRectangle(5, 16, 25, 4)
        
    def _funds_icon(self, dc: wx.PaintDC) -> None:
        dc.SetPen(wx.Pen(wx.Colour(self._icon_colour), 2))
        dc.SetBrush(wx.Brush(wx.Colour("#00000000")))
        font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        dc.SetTextForeground(self._icon_colour)
        dc.DrawText("$", 13, 5)
        
    def _database_icon(self, dc: wx.PaintDC) -> None:
        dc.SetPen(wx.Pen(wx.Colour('#00000000'), 1))
        dc.SetBrush(wx.Brush(self._icon_colour))
        dc.DrawRoundedRectangle(5, 7, 25, 4, 2)
        dc.DrawRoundedRectangle(5, 12, 25, 4, 2)
        dc.DrawRoundedRectangle(5, 17, 25, 4, 2)
        
    def applay_color_theme(self):
        self._text_colour = self._color_themes[self._current_theme]['text']
        self._icon_colour = self._color_themes[self._current_theme]['selection']
        self._pen_colour = self._color_themes[self._current_theme]['medium']
        self.SetBackgroundColour(self._color_themes[self._current_theme]['medium'])
        self.Refresh() 
       
        
        
        
        

        
        
        
        