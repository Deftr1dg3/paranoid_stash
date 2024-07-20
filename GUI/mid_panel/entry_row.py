#!/usr/bin/env python3


import wx
import ast

from manage_data import ManageData
from manage_data.manage_password.manage_password import ValidatePassword, StrengthSpecification, GeneratePassword
from GUI.base_panel import BasePanel
from GUI.right_panel.notes_panel import NotesPanel
from GUI.mid_panel.record_panel import RecordName, Username, Password, URL


class EntryRow(BasePanel):
    
    def __init__(self, parent: wx.ScrolledWindow, manage_date: ManageData, settings: dict, color_themes: dict, current_theme: str, entry: list) -> None:
        self._parent = parent 
        self._manage_data = manage_date
        self._settings = settings
        self._color_themes = color_themes
        self._current_theme = current_theme
    
        self._entry = entry
        self._size = ast.literal_eval(self._settings['mid_panel']['entry_row_size'])
        
        super().__init__(self._parent, size=self._size)
        
        self.is_selected = False
        
        self._text_colour = wx.Colour(self._color_themes[self._current_theme]['text'])
        self._selection_colour = wx.Colour(self._color_themes[self._current_theme]['selection'])
        self._background_colour = wx.Colour(self._color_themes[self._current_theme]['dark'])
        
        self._target_colour = self._selection_colour
        self._current_colour = self._background_colour
        
        self._colour_step = 1  # Determines the speed of color transition
        self._selection_speed = int(self._settings['mid_panel']['selection_speed'])
        self._colour_timer = wx.Timer(self)
        
        # Initializing visible objects and binding events
        self._init_ui()
        
        self.applay_color_theme(self._current_theme)
        
        self._bind_events()
        
        self.entry_rows.append(self)
        
    def _init_ui(self) -> None:
        """ Function initializing visible interface. """
        
        # Create main sizer
        main_box = wx.BoxSizer(wx.HORIZONTAL)
        
        # Create secondary sizers
        record_box = wx.BoxSizer(wx.VERTICAL)
        username_box = wx.BoxSizer(wx.VERTICAL)
        password_box = wx.BoxSizer(wx.VERTICAL)
        url_box = wx.BoxSizer(wx.VERTICAL)
        
        # Create GUI objects
        self._record_name = RecordName(self, self._manage_data, self._settings, self._color_themes, self._current_theme, self._entry[0])
        self._username = Username(self, self._manage_data, self._settings, self._color_themes, self._current_theme, self._entry[1])
        self._password = Password(self, self._manage_data, self._settings, self._color_themes, self._current_theme, self._entry[2])
        self._url = URL(self, self._manage_data, self._settings, self._color_themes, self._current_theme, self._entry[3])

        
        # Add GUI objects to secondary sizers
        record_box.Add(self._record_name, proportion=1, flag=wx.EXPAND | wx.LEFT, border=0)
        username_box.Add(self._username, proportion=1, flag=wx.EXPAND | wx.LEFT, border=0)
        password_box.Add(self._password, proportion=1, flag=wx.EXPAND | wx.LEFT, border=0)
        url_box.Add(self._url, proportion=1, flag=wx.EXPAND | wx.LEFT, border=0)
        record_box.AddStretchSpacer()
        
        # Add secondary sizers to the main sizer
        main_box.Add(record_box, proportion=1, flag=wx.EXPAND)
        main_box.Add(username_box, proportion=1, flag=wx.EXPAND)
        main_box.Add(password_box, proportion=1, flag=wx.EXPAND)
        main_box.Add(url_box, proportion=1, flag=wx.EXPAND)
        
        # Set main sizer to the panel
        self.SetSizer(main_box)
        
        # Refresh lauout
        self.Layout()
        
    def _bind_events(self) -> None:
        self._record_name.Bind(wx.EVT_LEFT_DOWN,self._on_left_click)
        self._username.Bind(wx.EVT_LEFT_DOWN,self._on_left_click)
        self._password.Bind(wx.EVT_LEFT_DOWN,self._on_left_click)
        self._url.Bind(wx.EVT_LEFT_DOWN,self._on_left_click)
        
        self._record_name.Bind(wx.EVT_RIGHT_DOWN,self._on_right_click)
        self._username.Bind(wx.EVT_RIGHT_DOWN,self._on_right_click)
        self._password.Bind(wx.EVT_RIGHT_DOWN,self._on_right_click)
        self._url.Bind(wx.EVT_RIGHT_DOWN,self._on_right_click)
        
        self.Bind(wx.EVT_TIMER, self._on_color_timer, self._colour_timer)
    
    def _on_left_click(self, event) -> None:
        if self._manage_data.selected_entry == id(self._entry):
            return
        if self._manage_data.selected_entry is not None:
            for entry in self.entry_rows:
                entry.deselect_entry()
        self.select_entry()
        self.body.right_panel.refresh() # type: ignore
        
    def _on_right_click(self, event) -> None:
        # self.select_entry()
        # right_click_menu = EntryRightClickMenu(self, self._command, self._entry)
        # position_in_widget = event.GetPosition()
        # position_on_screen = event.GetEventObject().ClientToScreen(position_in_widget)
        # position = self.ScreenToClient(position_on_screen)
        # self.PopupMenu(right_click_menu, position)
        ...
    
    def _smooth_select(self) -> None:
        self._target_colour = self._selection_colour
        self._colour_timer.Start(self._selection_speed)
        
    def _smooth_deselect(self) -> None:
        self._target_colour = self._background_colour
        self._colour_timer.Start(self._selection_speed)
        
    def _on_color_timer(self, event) -> None:
        # Calculate the new color
        r = self._move_towards(self._current_colour.Red(), self._target_colour.Red())
        g = self._move_towards(self._current_colour.Green(), self._target_colour.Green())
        b = self._move_towards(self._current_colour.Blue(), self._target_colour.Blue())

        # Set the new color
        self._current_colour = wx.Colour(r, g, b)
        self.SetBackgroundColour(self._current_colour)
        self.Refresh()

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
        
    def select_entry(self) -> None:
        self.is_selected = True
        self._manage_data.selected_entry = id(self._entry)
        self._smooth_select()
            
    def deselect_entry(self) -> None:
        self.is_selected = False
        self._smooth_deselect()
        
    def set_selected_colour(self) -> None:
        self.SetBackgroundColour(self._selection_colour)
        self.Refresh()
    
    def set_regular_colour(self) -> None:
        self.SetBackgroundColour(self._background_colour)
        self.Refresh()
        
    # def copy_record_name(self):
    #     self._record_name.copy_to_clipboard()
        
    # def copy_username(self) -> None:
    #     self._username.copy_to_clipboard()
        
    # def copy_password(self) -> None:
    #     self._password.copy_to_clipboard()
        
    # def copy_url(self) -> None:
    #     self._url.copy_to_clipboard()
        
    def applay_color_theme(self, theme_name: str):
        self._current_theme = theme_name
        self._text_colour = wx.Colour(self._color_themes[self._current_theme]['text'])
        self._selection_colour = wx.Colour(self._color_themes[self._current_theme]['selection'])
        self._background_colour = wx.Colour(self._color_themes[self._current_theme]['dark'])
        
        self._target_colour = self._selection_colour
        self._current_colour = self._background_colour
        
        if id(self._entry) == self._manage_data.selected_entry:
            self.set_selected_colour()
            self.is_selected = True
        else:
            self.set_regular_colour()
        
        self.Refresh()
    