#!/usr/bin/env python3


import wx
import sys

from GUI.base_panel import BasePanel
from GUI.menu_functions.menu_functions import MenuFunctions


class TopBarMenu(wx.MenuBar):
    def __init__(self, main_frame: wx.Frame, main_panel: BasePanel):
        super().__init__()
        self._main_frame = main_frame
        self._main_panel = main_panel
        
        self._options = self._main_panel.settings['top_bar_menu']['options']
        self._fields = list(self._main_panel.settings['top_bar_menu']['fields'].keys())
        
        self._functions = MenuFunctions(self._main_panel)
        
        self._init_menu()
        self._bind_events()
        
    def _init_menu(self):
        
        # Create "File" menu ------------------------------------------------------------------------------------------
        
        file_menu = wx.Menu()
        file_menu.Append(1, f"&{self._options['file']['new_category']}\t{self._options['file']['new_category_shortcut']}")
        file_menu.Append(2, f"&{self._options['file']['new_entry']}\t{self._options['file']['new_entry_shortcut']}")
        file_menu.Append(3, f"&{self._options['file']['remove_category']}\t{self._options['file']['remove_category_shortcut']}")
        file_menu.Append(4, f"&{self._options['file']['remove_entry']}\t{self._options['file']['remove_entry_shortcut']}")
        file_menu.Append(22, f"&{self._options['file']['rename_category']}")
        file_menu.AppendSeparator()
        file_menu.Append(5, f"&{self._options['file']['clear_category']}\t{self._options['file']['clear_category_shortcut']}")
        file_menu.AppendSeparator()
        file_menu.Append(11, f"&{self._options['file']['save_datafile_as']}")
        file_menu.Append(7, f"&{self._options['file']['show_datafile']}")
        file_menu.Append(8, f"&{self._options['file']['change_datafile_dir']}")
        file_menu.AppendSeparator()
        file_menu.Append(6, f"&{self._options['file']['change_password']}")
        file_menu.Append(10, f"&{self._options['file']['restore_from_backup']}")

        
        self.Append(file_menu, f"&{self._fields[0]}")

        # Create "File" menu ------------------------------------------------------------------------------------------
        
        # Create "Edit" menu ------------------------------------------------------------------------------------------
        
        edit_menu = wx.Menu()
        edit_menu.Append(41, f"&{self._options['edit']['copy_password']}\t{self._options['edit']['copy_password_shortcut']}")
        edit_menu.Append(42, f"&{self._options['edit']['copy_username']}\t{self._options['edit']['copy_username_shortcut']}")
        edit_menu.Append(43, f"&{self._options['edit']['copy_url']}\t{self._options['edit']['copy_url_shortcut']}")
        edit_menu.AppendSeparator()
        edit_menu.Append(31, f"&{self._options['edit']['undo']}\t{self._options['edit']['undo_shortcut']}")
        edit_menu.Append(32, f"&{self._options['edit']['redo']}\t{self._options['edit']['redu_shortcut']}")
        edit_menu.AppendSeparator()
        edit_menu.Append(33, f"&{self._options['edit']['category_up']}\t{self._options['edit']['category_up_shortcut']}")
        edit_menu.Append(34, f"&{self._options['edit']['category_down']}\t{self._options['edit']['category_down_shortcut']}")
        edit_menu.Append(35, f"&{self._options['edit']['entry_up']}\t{self._options['edit']['entry_up_shortcut']}")
        edit_menu.Append(36, f"&{self._options['edit']['entry_down']}\t{self._options['edit']['entry_down_shortcut']}")

        self.Append(edit_menu, f"&{self._fields[1]}")
        
        # Create "Edit" menu ------------------------------------------------------------------------------------------
        
        # Create "Help" menu ------------------------------------------------------------------------------------------
        
        help_menu = wx.Menu()
        help_menu.Append(61, f"&{self._options['help']['help']}\t{self._options['help']['help_shortcut']}")
        
        self.Append(help_menu, f"&{self._fields[2]}")
        
        # Create "Help" menu ------------------------------------------------------------------------------------------
        
    def _bind_events(self):
        
        # Bind "File" menu
        self._main_frame.Bind(wx.EVT_MENU, self._on_add_category, id=1)
        self._main_frame.Bind(wx.EVT_MENU, self._on_add_entry, id=2)
        self._main_frame.Bind(wx.EVT_MENU, self._on_remove_category, id=3)
        self._main_frame.Bind(wx.EVT_MENU, self._on_remove_entry, id=4)
        self._main_frame.Bind(wx.EVT_MENU, self._on_clear_category, id=5)
        self._main_frame.Bind(wx.EVT_MENU, self._on_change_file_password, id=6)
        self._main_frame.Bind(wx.EVT_MENU, self._on_show_datafile_in_folder, id=7)
        self._main_frame.Bind(wx.EVT_MENU, self._on_change_datafile_directory, id=8)
        self._main_frame.Bind(wx.EVT_MENU, self._on_change_datafile, id=9)
        self._main_frame.Bind(wx.EVT_MENU, self._on_restore_from_backup, id=10)
        self._main_frame.Bind(wx.EVT_MENU, self._on_save_datafile_as, id=11)
        
        self._main_frame.Bind(wx.EVT_MENU, self._on_rename_category, id=22)
        
        # Bind "Edit" menu
        self._main_frame.Bind(wx.EVT_MENU, self._on_copy_password, id=41)
        self._main_frame.Bind(wx.EVT_MENU, self._on_copy_username, id=42)
        self._main_frame.Bind(wx.EVT_MENU, self._on_copy_url, id=43)
        self._main_frame.Bind(wx.EVT_MENU, self._on_undo, id=31)
        self._main_frame.Bind(wx.EVT_MENU, self._on_redo, id=32)
        
        
        self._main_frame.Bind(wx.EVT_MENU, self._on_move_category_up, id=33)
        self._main_frame.Bind(wx.EVT_MENU, self._on_move_category_down, id=34)
        self._main_frame.Bind(wx.EVT_MENU, self._on_move_entry_up, id=35)
        self._main_frame.Bind(wx.EVT_MENU, self._on_move_entry_down, id=36)
        
        # Bind "Help" menu
        self._main_frame.Bind(wx.EVT_MENU, self._on_help, id=61)
        
        
    def _on_move_category_up(self, event) -> None:
        self._functions.move_category_up()
    
    def _on_move_category_down(self, event) -> None:
        self._functions.move_category_down()
        
    def _on_move_entry_up(self, event) -> None:
        self._functions.move_entry_up()
    
    def _on_move_entry_down(self, event) -> None:
        self._functions.move_entry_down()

    
    
    def _on_help(self, event) -> None:
        ...
        
    def _on_save_datafile_as(self, event) -> None:
        self._functions.save_datafile_as()
        
    def _on_restore_from_backup(self, event) -> None:
        ...
        
    def _on_change_datafile(self, event) -> None:
        ...
        
    def _on_change_datafile_directory(self, event) -> None:
        ...
        
    def _on_show_datafile_in_folder(self, event) -> None:
        ...
    
    def _on_change_file_password(self, event) -> None:
        self._functions.change_password()
        
        
    #  Edit funcs --------------------------------------------
    
    def _on_copy_password(self, event) -> None:
        self._functions.copy_password()
        
    def _on_copy_username(self, event) -> None:
        self._functions.copy_username()
    
    def _on_copy_url(self, event) -> None:
        self._functions.copy_record_name()


    #  File funcs --------------------------------------------

    def _on_add_category(self, event) -> None:
        self._functions.add_category()
        
    def _on_remove_category(self, event) -> None:
        self._functions.remove_category()
        
    def _on_rename_category(self, event) -> None:
        self._functions.rename_category()
    
    def _on_clear_category(self, event) -> None:
        self._functions.clear_category()

    def _on_add_entry(self, event) -> None:
        self._functions.add_entry()
    
    def _on_remove_entry(self, event) -> None:
        self._functions.remove_entry()
    
    def _on_undo(self, event) -> None:
        self._functions.undo()
    
    def _on_redo(self, event) -> None:
        self._functions.redu()