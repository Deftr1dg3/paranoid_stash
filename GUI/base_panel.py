from __future__ import annotations

import wx
from collections import deque

from manage_data import ManageData

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from GUI.body_panel import BodyPanel
    from GUI.top_panel import TopPanel
    from GUI.left_panel.category_row import CategoryRow
    from GUI.mid_panel.entry_row import EntryRow
    from GUI.menu_functions.menu_functions import MenuFunctions


class BasePanel(wx.Panel):
    instances = deque()
    category_rows: list[CategoryRow] = []
    entry_rows: list[EntryRow] = []
    
    selected_category_inst: CategoryRow | None = None
    selected_entry_inst: EntryRow | None = None
    
    body: BodyPanel 
    top_panel: TopPanel 
    
    _manage_data: ManageData 
    _settings: dict 
    _color_themes: dict 
    _current_theme: str 
    
    _functions: MenuFunctions
    
    def __new__(cls, *args, **kwargs):
        inst = super().__new__(cls, *args, **kwargs)
        cls.instances.append(inst)
        return inst

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # self._functions = MenuFunctions(self)

    @property
    def settings(self) -> dict:
        return self._settings
    
    @property
    def color_themes(self) -> dict:
        return self._color_themes

    @property
    def current_theme(self) -> str:
        return self._current_theme
    
    @property
    def functions(self) -> MenuFunctions:
        return self._functions

    @classmethod
    def set_body_panel(cls, inst: BodyPanel):
        cls.body = inst
        
    @classmethod
    def set_top_panel(cls, inst: TopPanel):
        cls.top_panel = inst
    
    @classmethod
    def set_manage_data(cls, inst: ManageData):
        cls._manage_data = inst
    
    @classmethod
    def set_settings(cls, inst: dict):
        cls._settings = inst
    
    @classmethod
    def set_color_themes(cls, inst: dict):
        cls._color_themes = inst
    
    @classmethod
    def set_current_theme(cls, inst: str):
        cls._current_theme = inst
    
    @classmethod
    def set_selected_category(cls, inst: CategoryRow | None):
        cls.selected_category_inst = inst
        
    @classmethod
    def set_selected_entry(cls, inst: EntryRow | None):
        cls.selected_entry_inst = inst
    
    @classmethod
    def set_menu_fucntions(cls, functions: 'MenuFunctions'):
        cls._functions = functions
        
    def refresh_left_panel(self):
        if self.body is None:
            return
        self.body.left_panel.refresh()
        
    def refresh_mid_panel(self):
        if self.body is None:
            return
        self.body.mid_panel.refresh()
    
    def refresh_right_panel(self):
        if self.body is None:
            return
        self.body.right_panel.refresh()
        
    def refresh_body_panel(self):
        if self.body is None:
            return
        self.refresh_left_panel()
        self.refresh_mid_panel()
        self.refresh_right_panel()
    
    def applay_color_theme(self):
        raise NotImplementedError(f'Function "apply_color_theme()" is not implemented in {self.__class__.__name__}.')

