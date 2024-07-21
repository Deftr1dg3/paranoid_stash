#!/usr/bin/env python3


import wx 

from manage_data import ManageData
from GUI.modals.popups import dialog_popup, get_input

class CategoryRightClickMenu(wx.Menu):
    
    def __init__(self, parent: wx.Panel, manage_date: ManageData, settings: dict, color_themes: dict, current_theme: str, body: BaseException) -> None:
        self._parent = parent 
        self._manage_data = manage_date
        self._settings = settings
        self._color_themes = color_themes
        self._current_theme = current_theme
        self._body = body
        
        self._config = self._settings['right_click_menu']['category']
        
        super().__init__()
        
        self._init_menu()
        self._bind_events()
        
    def _init_menu(self) -> None:
        
        self.Append(1, f"&{self._config['rename']}")
        self.AppendSeparator()
        self.Append(4, f"&{self._config['move_up']}\t{self._config['move_up_shortcut']}")
        self.Append(5, f"&{self._config['move_down']}\t{self._config['move_down_shortcut']}")
        self.AppendSeparator()
        self.Append(2, f"&{self._config['remove']}\t{self._config['remove_shortcut']}")
        self.Append(3, f"&{self._config['clear']}")

    def _bind_events(self) -> None:
        self.Bind(wx.EVT_MENU, self._on_rename_category, id=1)
        self.Bind(wx.EVT_MENU, self._on_remove_category, id=2)
        self.Bind(wx.EVT_MENU, self._on_clear_category, id=3)
        self.Bind(wx.EVT_MENU, self._on_move_category_up, id=4)
        self.Bind(wx.EVT_MENU, self._on_move_category_down, id=5)
    
    def _refresh_body_panel(self):
        self._body.left_panel.refresh() # type: ignore
        self._body.mid_panel.refresh() # type: ignore
        self._body.right_panel.refresh() # type: ignore
        
    def _on_move_category_up(self, event) -> None:
        self._manage_data.move_category()
        self._refresh_body_panel()

    def _on_move_category_down(self, event) -> None:
        self._manage_data.move_category(direction=1)
        self._refresh_body_panel()
        
    def _on_rename_category(self, event) -> None:
        color = self._color_themes[self._current_theme]['medium']
        new_category = get_input(color=color, hint="Enter desired category name:", title="New Category")
        if new_category is None or new_category == "":
            return 
        self._manage_data.rename_category(new_category)
        self._refresh_body_panel()
        
    def _on_remove_category(self, event) -> None:
        message = self._config['remove_dialog']['message']
        title = self._config['remove_dialog']['title']
        confirmed = dialog_popup(message=message, title=title)
        if confirmed:
            self._manage_data.delete_category()
            self._refresh_body_panel()
    
    def _on_clear_category(self, event) -> None:
        message = self._config['clear_dialog']['message']
        title = self._config['clear_dialog']['title']
        confirmed = dialog_popup(message=message, title=title)
        if confirmed:
            self._manage_data.clear_category()
            self._refresh_body_panel()
           