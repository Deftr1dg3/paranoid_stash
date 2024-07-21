import wx
import ast

from manage_data import ManageData

from GUI.base_panel import BasePanel
from GUI.left_panel.category_row import CategoryRow

class LeftPanel(BasePanel):
    def __init__(self, parent: wx.Panel, manage_date: ManageData, settings: dict, color_themes: dict, current_theme: str) -> None:
        self._parent = parent 
        self._manage_data = manage_date
        self._settings = settings
        self._color_themes = color_themes
        self._current_theme = current_theme
        
        self._size = ast.literal_eval(self._settings['left_panel']['size'])
        self._scroll_settings = ast.literal_eval(self._settings['left_panel']['scroll_settings'])
        
        super().__init__(self._parent, size=self._size)
        
        self._scroll_position = (0, 0)
        
        # self._main_box = wx.BoxSizer(wx.VERTICAL)
        self._init_ui()
        self.applay_color_theme(self._current_theme)
        
        # self._bind_events()
        
        
    def _init_ui(self):
        """ Function initializing visible interface. """
        
        # Create main sizer
        main_box = wx.BoxSizer(wx.VERTICAL)
        
        # Create ScrolledWindow
        self.scroll = wx.ScrolledWindow(self, -1, style=wx.VSCROLL)
        self.scroll.SetScrollbars(*self._scroll_settings)
        self.scroll.SetScrollRate(30, 30)
        
        # Create secondary sizer for ScrolledWindow
        scroll_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Create GUI objects
        for category in self._manage_data.all_categories():
            self._display_category(self.scroll, scroll_sizer, category) 
        
        # Add sizer to ScrolledWindow
        self.scroll.SetSizer(scroll_sizer)
        
        # Add scroll window to the main sizer
        main_box.Add(self.scroll, 1, wx.EXPAND)
        
        # Set main sizer to the panel
        self.SetSizer(main_box)
        
        # Refresh layout
        self.Layout()
        
        # Scroll to selected entity
        self._scroll_to_selected()

    def _scroll_to_selected(self):
        if self._manage_data.selected_category is not None:
            index = self._manage_data.get_category_index(self._manage_data.selected_category)
            self.scroll.Scroll((0, index))
        
    def _display_category(self, scroll, scroll_sizer, category) -> None:
        category_row = CategoryRow(scroll, self._manage_data, self._settings, self._color_themes, self._current_theme, category)
        # self._category_rows[category.id] = category_row
        scroll_sizer.Add(category_row, 0, wx.EXPAND)
        
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
        self.category_rows.clear()
        self._init_ui()
        self.Refresh()
        
    def applay_color_theme(self, theme_name: str):
        self._current_theme= theme_name
        self.SetBackgroundColour(wx.Colour(self._color_themes[self._current_theme]['medium']))
        self.Refresh()
        
        