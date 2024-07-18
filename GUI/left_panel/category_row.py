#!/usr/bin/env python3


import wx
import ast 

from GUI.base_panel import BasePanel
from GUI.left_panel.category_panel import CategoryNamePanel
from GUI.left_panel.icons.icons import IconPanel
from GUI.left_panel.icons.icons_names import IconNames
from manage_data import ManageData

class CategoryRow(BasePanel):
    
    _row_instances = []
    
    def __init__(self, parent: wx.Panel, manage_date: ManageData, settings: dict, color_themes: dict, current_theme: str, category_name: str) -> None:
        self._parent = parent 
        self._manage_data = manage_date
        self._settings = settings
        self._color_themes = color_themes
        self._current_theme = current_theme
        
        self._category_name = category_name
        self._size = ast.literal_eval(self._settings['left_panel']['category_row_size'])
        
        self.is_selected = False
        
        super().__init__(self._parent, size=self._size)
        
        # Setting colours
        self._text_colour = self._color_themes[self._current_theme]['text']
        self._selection_colour = self._color_themes[self._current_theme]['selection']
        
        # Defining target and current colours
        self._target_colour = self._selection_colour
        self._current_colour = self._text_colour
        
        # Defining colour timer and colour changing step
        self._colour_step = 2  # Determines the speed of color transition
        self._selection_speed = int(self._settings['left_panel']['selection_speed'])
        self._colour_timer = wx.Timer(self)
        
        # Initializing visible objects and binding events
        self._init_ui()
        self._bind_events()
        
        self.applay_color_theme(self._current_theme)
        
        self._row_instances.append(self)
        
    def _init_ui(self) -> None:
        """ Function initializing visible interface. """
        
        # Create main sizer
        main_box = wx.BoxSizer(wx.HORIZONTAL)
        
        # Create secondary sizers
        icon_box = wx.BoxSizer(wx.VERTICAL)
        category_box = wx.BoxSizer(wx.VERTICAL)
        
        set(self._settings['left_panel']['icon_email'].split(','))
        
        # Create Icon, depending on the category name
        if set(self._category_name.lower().split()).intersection(set(self._settings['left_panel']['icon_email'].split(','))):
            self._icon_name = IconNames.EMAIL
            
        elif set(self._category_name.lower().split()).intersection(set(self._settings['left_panel']['icon_devops'].split(','))):
            self._icon_name = IconNames.DEVOPS
            
        elif set(self._category_name.lower().split()).intersection(set(self._settings['left_panel']['icon_database'].split(','))):
            self._icon_name = IconNames.DATABASE
            
        elif set(self._category_name.lower().split()).intersection(set(self._settings['left_panel']['icon_crypto'].split(','))):
            self._icon_name = IconNames.CRYPTO
        
        elif set(self._category_name.lower().split()).intersection(set(self._settings['left_panel']['icon_funds'].split(','))):
            self._icon_name = IconNames.FUNDS
        
        elif set(self._category_name.lower().split()).intersection(set(self._settings['left_panel']['icon_payments'].split(','))):
            self._icon_name = IconNames.PAYMENTS
            
        elif set(self._category_name.lower().split()).intersection(set(self._settings['left_panel']['icon_internet'].split(','))):
            self._icon_name = IconNames.INTERNET
            
        else:
            self._icon_name = IconNames.FOLDER
        
        self._display_icon = IconPanel(self, self._settings, self._color_themes, self._current_theme, self._icon_name)
        # Create category panel object
        self._display_category = CategoryNamePanel(self, self._manage_data, self._settings, self._color_themes, self._current_theme, self._category_name)
        
        # Add gui objects to secondary sizers
        icon_box.Add(self._display_icon)
        category_box.Add(self._display_category)
        
        # Add secondary sizers to the main sizer
        main_box.Add(icon_box)
        main_box.Add(category_box)
        
        # Set main sizer to the panel
        self.SetSizer(main_box)
        
        # Refresh lauout
        self.Layout()
        
    def _bind_events(self) -> None:
        # self._display_icon.Bind(wx.EVT_LEFT_DOWN, self._on_left_click)
        # self._display_icon.Bind(wx.EVT_RIGHT_DOWN, self._on_right_click)
        
        self._display_category.Bind(wx.EVT_LEFT_DOWN, self._on_left_click)
        self._display_category.Bind(wx.EVT_RIGHT_DOWN, self._on_right_click)

        self.Bind(wx.EVT_TIMER, self._on_color_timer, self._colour_timer)
        
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_mouse_over)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_mouse_leave)
    
    def _on_left_click(self, event) -> None:
        for instance in self._row_instances:
            if instance.is_selected:
                instance.is_selected = False 
                instance.deselect_row()
        self.is_selected = True 
        self._manage_data.selected_category = self._category_name
        self.select_row()
        
    def _on_right_click(self, event) -> None:
        # self._on_left_click(None)
        # right_click_menu = CategoryRightClickMenu(self, self._command, self._category)
        # position_in_widget = event.GetPosition()
        # position_on_screen = event.GetEventObject().ClientToScreen(position_in_widget)
        # position = self.ScreenToClient(position_on_screen)
        # self.PopupMenu(right_click_menu, position)
        ...
    
    def on_mouse_over(self, event) -> None:
        if not self.is_selected:
            self._target_colour = self._selection_colour
            self._colour_timer.Start(self._selection_speed)
        
    def on_mouse_leave(self, event) -> None:
        if not self.is_selected:
            self._target_colour = self._text_colour
            self._colour_timer.Start(self._selection_speed)
        
    def _on_color_timer(self, event) -> None:
        if not self.is_selected:
            # Calculate the new color
            r = self._move_towards(self._current_colour.Red(), self._target_colour.Red())
            g = self._move_towards(self._current_colour.Green(), self._target_colour.Green())
            b = self._move_towards(self._current_colour.Blue(), self._target_colour.Blue())

            # Set the new color
            self._current_colour = wx.Colour(r, g, b)
            self._display_category.set_text_colour(self._current_colour)
            # self.Refresh()

            # Stop the timer if the target color has been reached
            if self._current_colour.Red() == self._target_colour.Red() and \
            self._current_colour.Green() == self._target_colour.Green() and \
            self._current_colour.Blue() == self._target_colour.Blue():
                self._colour_timer.Stop()

    def _move_towards(self, current: int, target: int) -> int:
        # Helper function to move a color channel value towards a target value
        if current < target:
            return min(current + self._colour_step, target)
        elif current > target:
            return max(current - self._colour_step, target)
        else:
            return current
        
    def select_row(self) -> None:
        self._colour_timer.Stop()
        self.is_selected = True
        self._display_category.set_text_colour(self._selection_colour)
        self._current_colour = self._selection_colour
            
    def deselect_row(self) -> None:
        self.is_selected = False
        self._target_colour = self._text_colour
        self.on_mouse_leave(None)
    
    def applay_color_theme(self, theme_name: str):
        self._current_theme = theme_name
         # Setting colours
        self._text_colour = wx.Colour(self._color_themes[self._current_theme]['text'])
        self._selection_colour = wx.Colour(self._color_themes[self._current_theme]['selection'])
        
        # Defining target and current colours
        self._target_colour = wx.Colour(self._selection_colour)
        self._current_colour = wx.Colour(self._text_colour)
        
        if self._category_name == self._manage_data.selected_category:
            self.select_row()
    
        self.SetBackgroundColour(self._color_themes[self._current_theme]['medium'])
        self.Refresh()
        