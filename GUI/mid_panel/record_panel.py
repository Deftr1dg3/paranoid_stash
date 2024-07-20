#!/usr/bin/env python3


import wx
import ast
import pyperclip

from manage_data import ManageData
from manage_data.manage_password.manage_password import ValidatePassword, StrengthSpecification, GeneratePassword
from GUI.base_panel import BasePanel
from GUI.right_panel.notes_panel import NotesPanel



class BaseRecordPanel(BasePanel):
    def __init__(self, parent: wx.Panel, manage_data: ManageData, settings: dict, color_themes: dict, current_theme: str, record_value: str) -> None:
        self._parent = parent 
        self._manage_data = manage_data
        self._settings = settings
        self._color_themes = color_themes
        self._current_theme = current_theme
        
        self._record_value = record_value
        
        self._displayed_str_length = int(self._settings['mid_panel']['display_string_len'])
        self._displayed_password_length = int(self._settings['mid_panel']['display_pssword_placeholder_len'])
        self._extra_characters_replacement = self._settings['mid_panel']['replacement_characters']
        
        super().__init__(self._parent)
        
        self._text_colour = wx.Colour(self._color_themes[self._current_theme]['text'])
        self._selection_colour = wx.Colour(self._color_themes[self._current_theme]['selection'])
        self._current_colour = wx.Colour(self._color_themes[self._current_theme]['text'])
        
        self._colour_step = 1  # Determines the speed of color transition
        self._selection_speed = int(self._settings['mid_panel']['selection_speed'])
        self._colour_timer = wx.Timer(self)
        
        self._init_ui()
        self.applay_color_theme(self._current_theme)
        
        self._bind_events()
        
    def _init_ui(self) -> None:
        """ Function initializing visible interface. """
        
        # Create main sizer
        main_box = wx.BoxSizer(wx.HORIZONTAL)
        
        # Create GUI object
        self._display_value = wx.StaticText(self, label=self._format_category_name(self._record_value))
        # self._display_value.SetForegroundColour(self._text_colour)
        
        # Add GUI object to the main sizer
        main_box.Add(self._display_value, 0, wx.TOP | wx.LEFT, 6)
        
        # Set main sizer to the panel
        self.SetSizer(main_box)
        
        # Refresh lauout
        self.Layout()
    
    def _bind_events(self):
        self.Bind(wx.EVT_LEFT_DCLICK, self._on_left_dclick)
        self.Bind(wx.EVT_TIMER, self._on_color_timer)
        
    def copy_to_clipboard(self) -> None:
        pyperclip.copy(self._record_value)
        # launch_copy_poup(self._command.top)
        
    def _change_colour(self) -> None:
        self._set_text_colour(self._selection_colour)
        self._current_colour = self._selection_colour
        self._colour_timer.Start(10)
    
    def _on_left_dclick(self, event):
        self._change_colour()
        self.copy_to_clipboard()
        
    def _on_color_timer(self, event) -> None:
        # Calculate the new color
        r = self._move_towards(self._current_colour.Red(), self._text_colour.Red())
        g = self._move_towards(self._current_colour.Green(), self._text_colour.Green())
        b = self._move_towards(self._current_colour.Blue(), self._text_colour.Blue())

        # Set the new color
        self._current_colour = wx.Colour(r, g, b)
        self._set_text_colour(self._current_colour)

        # Stop the timer if the target color has been reached
        if self._current_colour.Red() == self._text_colour.Red() and \
        self._current_colour.Green() == self._text_colour.Green() and \
        self._current_colour.Blue() == self._text_colour.Blue():
            self._colour_timer.Stop()

    def _move_towards(self, current: int, target: int) -> int:
        # Helper function to move a color channel value towards a target value
        if current < target:
            return min(current + self._colour_step, target)
        elif current > target:
            return max(current - self._colour_step, target)
        else:
            return current 
        
    def _format_category_name(self, record_value: str) -> str:
        if len(record_value) > self._displayed_str_length:
            record_value = record_value[:self._displayed_str_length] + self._extra_characters_replacement
        return record_value
    
    def _set_text_colour(self, colour: wx.Colour) -> None:
        self._display_value.SetForegroundColour(colour)
        self.Refresh() 
    
    def applay_color_theme(self, theme_name: str):
        self._current_theme = theme_name
        self._text_colour = wx.Colour(self._color_themes[self._current_theme]['text'])
        self._selection_colour = wx.Colour(self._color_themes[self._current_theme]['selection'])
        self._current_colour = wx.Colour(self._color_themes[self._current_theme]['text'])
        
        # self.SetBackgroundColour(self._color_themes[self._current_theme]['dark'])
        self._display_value.SetForegroundColour(self._text_colour)
        
        self.Refresh()
    

class RecordName(BaseRecordPanel):
    ...
    
    
class Username(BaseRecordPanel):
    ...
    
    
class Password(BaseRecordPanel):
    def _format_category_name(self, record_value: str) -> str:
        value_to_display = "*" * self._displayed_password_length
        return value_to_display
    
    
class URL(BaseRecordPanel):
    ...