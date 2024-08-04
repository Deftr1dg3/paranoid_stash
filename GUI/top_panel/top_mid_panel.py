#!/usr/bin/env python3

import wx

from GUI.base_panel import BasePanel
# from GUI.menu_functions.menu_functions import MenuFunctions

class TopMidPanel(BasePanel):
    def __init__(self, parent: BasePanel) -> None:
        super().__init__(parent)
        
        self._search_field_size = self._settings['top_panel']['top_mid_panel']['search_field_size']
        self._new_entry_label = self._settings['top_panel']['top_mid_panel']['new_entry_label']
        self._search_placeholder = self._settings['top_panel']['top_mid_panel']['search_placeholder']
        
        self._foreground_color = wx.Colour(self._color_themes[self._current_theme]['text'])
        
        # self._functions = MenuFunctions(self)
        
        self._init_ui()
        self._bind_events()
        
        self.applay_color_theme()
        
    def _init_ui(self) -> None:
        # Create main sizer
        self._main_box = wx.BoxSizer(wx.HORIZONTAL)
        
        # Create secondary sizers, that will be added to the main sizer.
        button_box = wx.BoxSizer(wx.VERTICAL)
        search_box = wx.BoxSizer(wx.VERTICAL)
        
        self._new_entry = wx.Button(self, label=self._new_entry_label)

        self._search = wx.TextCtrl(self, size=self._search_field_size, style=wx.TE_PROCESS_ENTER)
        self._search.SetHint(self._search_placeholder)

        # Add created objects to the sizers
        button_box.Add(self._new_entry, 0, wx.EXPAND | wx.LEFT, 10)
        search_box.Add(self._search, 0, wx.EXPAND)
        
        # Add sizers to the main sizer.
        self._main_box.Add(button_box, 0, wx.ALL | wx.EXPAND, 5)
        self._main_box.AddStretchSpacer()
        
        self._main_box.Add(search_box, 0, wx.ALL | wx.EXPAND, 3)
        
        # Set main sizer to the panel
        self.SetSizer(self._main_box)
        
        # Refresh layout
        self.Layout()
        
        self._dummy_panel = wx.Panel(self, size=(0, 0))
        
    def _bind_events(self) -> None:
        self._new_entry.Bind(wx.EVT_BUTTON, self._add_entry)
        self._search.Bind(wx.EVT_TEXT, self._on_search)
        # self._search.Bind(wx.EVT_SET_FOCUS, self._on_search)
        self._search.Bind(wx.EVT_TEXT_ENTER, self._on_enter_pressed)
    
    def _on_enter_pressed(self, event) -> None:
        self.deselect_search()
        self._on_search(None)
        event.Skip()
        
    def deselect_search(self):
        self._dummy_panel.SetFocus()

    def _add_entry(self, event) -> None:
        self._functions.add_entry()
            
    def get_query(self):
        return self._search.GetValue()
        
    def _on_search(self, event) -> None:
        self._functions.search()
        
    def applay_color_theme(self) -> None:
        self.SetBackgroundColour(wx.Colour(self._color_themes[self._current_theme ]['medium']))
        self._search.SetForegroundColour(wx.Colour(self._color_themes[self._current_theme ]['text']))
        self._search.SetBackgroundColour(wx.Colour(self._color_themes[self._current_theme ]['input_background']))
        self.Refresh()
        