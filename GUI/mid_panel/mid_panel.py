#!/usr/bin/env python3

import wx 

from GUI.base_panel import BasePanel
from GUI.mid_panel.entry_row import EntryRow


class MidPanel(BasePanel):
    def __init__(self, parent: BasePanel) -> None:
        self._parent = parent 
        
        super().__init__(self._parent)
        
        self._scroll_settings = self._settings['mid_panel']['scroll_settings']
        
        # Initializing visible objects
        self._init_ui()
        self.applay_color_theme()
        
    def _init_ui(self):
        """ Function initializing visible interface. """
        
        # Create main sizer
        self._main_box = wx.BoxSizer(wx.VERTICAL)
        
        # Create ScrolledWindow
        self.scroll = wx.ScrolledWindow(self, -1)
        self.scroll.SetScrollbars(*self._scroll_settings)
        self.scroll.SetScrollRate(30, 30)
        
        # Sizer for ScrolledWindow.
        scroll_sizer = wx.BoxSizer(wx.VERTICAL)
        
        if self._manage_data.search_results is not None:
            entries = self._manage_data.search_results
        else:
            if self._manage_data.selected_category is not None:
                entries = self._manage_data.get_category_data(self._manage_data.selected_category)
            else:
                entries = []
            
        for entry in entries:
            # Create visible EntryRow object
            self._display_entry(scroll_sizer, entry)
            # print(f'{entry = }')
                
        # Add sizer to ScrolledWindow
        self.scroll.SetSizer(scroll_sizer)
        
        # Add scroll window to the main sizer
        self._main_box.Add(self.scroll, 1, wx.EXPAND)
        
        # Set main sizer to the panel
        self.SetSizer(self._main_box)
        
        # Refresh lauout
        self.Layout()

        # Scroll to selected entity
        self._scroll_to_selected()
    
    def _scroll_to_selected(self):
        if self._manage_data.selected_entry is not None:
            index = self._manage_data.get_entry_index(self._manage_data.selected_entry)
            self.scroll.Scroll((0, index))
        
    def _display_entry(self, scroll_sizer, entry: list) -> None:
        entry_row = EntryRow(self.scroll, entry)
        scroll_sizer.Add(entry_row, 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 1)
        
    def _clear_categories(self):
        # Get the sizer from the ScrolledWindow
        scroll_sizer = self.scroll.GetSizer()
        
        # Destroy all children of the ScrolledWindow
        for child in self.scroll.GetChildren():
            child.Destroy()
            
        # Clear the sizer
        scroll_sizer.Clear(True)
        
        # Layout the sizer
        scroll_sizer.Layout()
        self.Layout() 
        
    def refresh(self):
        self._clear_categories()
        self.entry_rows.clear()
        self._init_ui()
    
    def applay_color_theme(self):
        self._text_colour = self._color_themes[self._current_theme]['text']
        self._input_background_colour = self._color_themes[self._current_theme]['input_background']
        self.SetBackgroundColour(self._color_themes[self._current_theme]['dark'])
        self.Refresh()