#!/usr/bin/env python3


import wx 


from GUI.base_panel import BasePanel
from GUI.menu_functions.menu_functions import MenuFunctions


class CategoryRightClickMenu(wx.Menu):
    
    def __init__(self, parent: BasePanel) -> None:
        super().__init__()
        
        self._functions = MenuFunctions(parent)
        
        self._config = self._functions.settings['menu']['category']
        
        
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
    
        
    def _on_move_category_up(self, event) -> None:
        self._functions.move_category_up()

    def _on_move_category_down(self, event) -> None:
        self._functions.move_category_down()
        
    def _on_rename_category(self, event) -> None:
        self._functions.rename_category()
        
    def _on_remove_category(self, event) -> None:
        self._functions.remove_category()
    
    def _on_clear_category(self, event) -> None:
        self._functions.clear_category()
           