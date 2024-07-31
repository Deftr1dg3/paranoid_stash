#!/usr/bin/env python3


import wx 

from GUI.base_panel import BasePanel
from GUI.menu_functions.menu_functions import MenuFunctions

class EntryRightClickMenu(wx.Menu):
    def __init__(self, parent: BasePanel) -> None:
        super().__init__()
        
        self._parent = parent
        self._functions = MenuFunctions(parent)
        self._config = self._functions.settings['menu']['entry']
        self._options = self._parent.settings['top_bar_menu']['options']
        
        self._init_menu()
        self._bind_events()
        
    def _init_menu(self) -> None:
        
        # Menu inside menu ----------------------------------------
        
        # Move entry to another category ------------
        self._id_category = {}
        categories_menu = wx.Menu()
        for category in self._parent._manage_data.all_categories():
            item_id = wx.NewIdRef()
            categories_menu.Append(item_id, f"{category}")
            self._id_category[item_id] = category
            self.Bind(wx.EVT_MENU, self._on_move_entry_to, id=item_id)
        
        # Main menu ------------------------------------------------
        
        self.Append(421, f"&{self._config['copy_password']}\t{self._config['copy_password_shortcut']}")
        self.Append(422, f"&{self._config['copy_username']}\t{self._config['copy_username_shortcut']}")
        self.Append(423, f"&{self._config['copy_url']}\t{self._config['copy_url_shortcut']}")
        self.AppendSeparator()
        self.Append(39, f"&{self._options['edit']['move_entry_to']}", categories_menu)
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
        
    def _on_move_entry_to(self, event: wx.Event) -> None:
        event_id = event.GetId()
        category = self._id_category[event_id]
        self._functions.move_entry_to_category(category=category)
        
    def _on_move_entry_up(self, event: wx.Event) -> None:
        self._functions.move_entry_up()
    
    def _on_move_entry_down(self, event: wx.Event) -> None:
        self._functions.move_entry_down() 
        
    def _on_copy_password(self, event: wx.Event) -> None:
        self._functions.copy_password()
        
    def _on_copy_username(self, event: wx.Event) -> None:
        self._functions.copy_username()
    
    def _on_copy_url(self, event: wx.Event) -> None:
        self._functions.copy_url()
               
    def _on_remove_entry(self, event: wx.Event) -> None:
        self._functions.remove_entry()
        