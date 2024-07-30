#!/usr/bin/env python3


import wx 

from GUI.base_panel import BasePanel
from GUI.menu_functions.menu_functions import MenuFunctions

class EntryRightClickMenu(wx.Menu):
    def __init__(self, parent: BasePanel) -> None:
        super().__init__()
        
        self._functions = MenuFunctions(parent)
        
        self._config = self._functions.settings['menu']['entry']
        
        self._init_menu()
        self._bind_events()
        
    def _init_menu(self) -> None:
        self.Append(421, f"&{self._config['copy_password']}\t{self._config['copy_password_shortcut']}")
        self.Append(422, f"&{self._config['copy_username']}\t{self._config['copy_username_shortcut']}")
        self.Append(423, f"&{self._config['copy_url']}\t{self._config['copy_url_shortcut']}")
        self.AppendSeparator()
        self.Append(35, f"&{self._config['entry_up']}\t{self._config['entry_up_shortcut']}")
        self.Append(36, f"&{self._config['entry_down']}\t{self._config['entry_down_shortcut']}")
        self.AppendSeparator()
        self.Append(33, f"&{self._config['remove_entry']}\t{self._config['remove_entry_shortcut']}")
   
    def _bind_events(self) -> None:
        self.Bind(wx.EVT_MENU, self._on_copy_password, id=421)
        self.Bind(wx.EVT_MENU, self._on_copy_username, id=422)
        self.Bind(wx.EVT_MENU, self._on_copy_url, id=423)
        self.Bind(wx.EVT_MENU, self._on_remove_entry, id=33)
        self.Bind(wx.EVT_MENU, self._on_move_entry_up, id=35)
        self.Bind(wx.EVT_MENU, self._on_move_entry_down, id=36)
        
    def _on_move_entry_up(self, event) -> None:
        self._functions.move_entry_up()
    
    def _on_move_entry_down(self, event) -> None:
        self._functions.move_entry_down() 
        
    def _on_copy_password(self, event) -> None:
        self._functions.copy_password()
        
    def _on_copy_username(self, event) -> None:
        self._functions.copy_username()
    
    def _on_copy_url(self, event) -> None:
        self._functions.copy_url()
               
    def _on_remove_entry(self, event) -> None:
        self._functions.remove_entry()
        