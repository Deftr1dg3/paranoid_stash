#!/usr/bin/env python3


import wx

from GUI.base_panel import BasePanel
# from GUI.menu_functions.menu_functions import MenuFunctions


class TopBarMenu(wx.MenuBar):
    def __init__(self, main_frame: wx.Frame, main_panel: BasePanel):
        super().__init__()
        self._main_frame = main_frame
        self._base_panel = main_panel
        
        self._options = self._base_panel.settings['top_bar_menu']['options']
        self._fields = list(self._base_panel.settings['top_bar_menu']['fields'].keys())
        
        self._moving_entity = False
        
        self._functions = self._base_panel.functions
        
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
        file_menu.Append(38, f"&{self._options['file']['copy_datafile_path']}")
        # file_menu.Append(8, f"&{self._options['file']['change_datafile_dir']}")
        file_menu.Append(9, f"&{self._options['file']['load_from_datafile']}")
        file_menu.AppendSeparator()
        file_menu.Append(40, f"&{self._options['file']['cretae_backup']}\t{self._options['file']['cretae_backup_shortcut']}")
        file_menu.AppendSeparator()
        file_menu.Append(6, f"&{self._options['file']['change_password']}")
        file_menu.Append(10, f"&{self._options['file']['restore_from_backup']}")

        
        self.Append(file_menu, f"&{self._fields[0]}")

        # Create "File" menu ------------------------------------------------------------------------------------------
        
        # Create "Edit" menu ------------------------------------------------------------------------------------------
        
        
        # Menu inside menu ----------------------------------------
        
        # Move entry to another category ------------
        
        self._id_category = {}
        categories_menu = wx.Menu()
        for category in self._base_panel._manage_data.all_categories():
            item_id = wx.NewIdRef()
            categories_menu.Append(item_id, f"{category}")
            self._id_category[item_id] = category
            self._main_frame.Bind(wx.EVT_MENU, self._on_move_entry_to, id=item_id)
        
        # Main menu ------------------------------------------------
        
        edit_menu = wx.Menu()
        edit_menu.Append(41, f"&{self._options['edit']['copy_password']}\t{self._options['edit']['copy_password_shortcut']}")
        edit_menu.Append(42, f"&{self._options['edit']['copy_username']}\t{self._options['edit']['copy_username_shortcut']}")
        edit_menu.Append(43, f"&{self._options['edit']['copy_url']}\t{self._options['edit']['copy_url_shortcut']}")
        edit_menu.AppendSeparator()
        edit_menu.Append(31, f"&{self._options['edit']['undo']}\t{self._options['edit']['undo_shortcut']}")
        edit_menu.Append(32, f"&{self._options['edit']['redo']}\t{self._options['edit']['redu_shortcut']}")
        edit_menu.AppendSeparator()
        # edit_menu.Append(37, f"&{self._options['edit']['search']}\t{self._options['edit']['search_shortcut']}")
        edit_menu.Append(39, f"&{self._options['edit']['move_entry_to']}", categories_menu)
        edit_menu.AppendSeparator()
        edit_menu.Append(33, f"&{self._options['edit']['category_up']}\t{self._options['edit']['category_up_shortcut']}")
        edit_menu.Append(34, f"&{self._options['edit']['category_down']}\t{self._options['edit']['category_down_shortcut']}")
        edit_menu.Append(35, f"&{self._options['edit']['entry_up']}\t{self._options['edit']['entry_up_shortcut']}")
        edit_menu.Append(36, f"&{self._options['edit']['entry_down']}\t{self._options['edit']['entry_down_shortcut']}")

        self.Append(edit_menu, f"&{self._fields[1]}")
        
        # Create "Edit" menu ------------------------------------------------------------------------------------------
        
        # Create "Encryption" menu ------------------------------------------------------------------------------------------
        
        encryption_menu = wx.Menu()
        encryption_menu.Append(44, f"&{self._options['file_encryption']['encrypt_file']}\t{self._options['file_encryption']['encrypt_file_shortcut']}")
        # encryption_menu.Append(45, f"&{self._options['file_encryption']['decrypt_file']}")
        
        self.Append(encryption_menu, f"&{self._fields[2]}")
        
        # Create "Encryption" menu ------------------------------------------------------------------------------------------
        
        # Create "Help" menu ------------------------------------------------------------------------------------------
        
        help_menu = wx.Menu()
        help_menu.Append(61, f"&{self._options['help']['help']}\t{self._options['help']['help_shortcut']}")
        
        self.Append(help_menu, f"&{self._fields[3]}")
        
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
        # self._main_frame.Bind(wx.EVT_MENU, self._on_change_datafile_directory, id=8)
        self._main_frame.Bind(wx.EVT_MENU, self._on_load_from_datafile, id=9)
        self._main_frame.Bind(wx.EVT_MENU, self._on_restore_from_backup, id=10)
        self._main_frame.Bind(wx.EVT_MENU, self._on_save_datafile_as, id=11)
        
        self._main_frame.Bind(wx.EVT_MENU, self._on_rename_category, id=22)
        
        # Bind "Edit" menu
        self._main_frame.Bind(wx.EVT_MENU, self._on_copy_password, id=41)
        self._main_frame.Bind(wx.EVT_MENU, self._on_copy_username, id=42)
        self._main_frame.Bind(wx.EVT_MENU, self._on_copy_url, id=43)
        self._main_frame.Bind(wx.EVT_MENU, self._on_undo, id=31)
        self._main_frame.Bind(wx.EVT_MENU, self._on_redo, id=32)
        # self._main_frame.Bind(wx.EVT_MENU, self._on_search, id=37)
        self._main_frame.Bind(wx.EVT_MENU, self._on_copy_datafile_path, id=38)
        # self._main_frame.Bind(wx.EVT_MENU, self._on_move_entry_to, id=39)
        self._main_frame.Bind(wx.EVT_MENU, self._on_create_backup, id=40)
        
        self._main_frame.Bind(wx.EVT_MENU, self._on_move_category_up, id=33)
        self._main_frame.Bind(wx.EVT_MENU, self._on_move_category_down, id=34)
        self._main_frame.Bind(wx.EVT_MENU, self._on_move_entry_up, id=35)
        self._main_frame.Bind(wx.EVT_MENU, self._on_move_entry_down, id=36)
        
        # Bind "file encryption"
        self._main_frame.Bind(wx.EVT_MENU, self._on_file_encryption, id=44)
        # self._main_frame.Bind(wx.EVT_MENU, self._on_file_decrypt, id=45)
        
        # Bind "Help" menu
        self._main_frame.Bind(wx.EVT_MENU, self._on_help, id=61)
    


    #  File funcs --------------------------------------------

    def _on_add_category(self, event: wx.Event) -> None:
        self._functions.add_category()
    
    def _on_add_entry(self, event: wx.Event) -> None:
        self._functions.add_entry()
        
    def _on_remove_category(self, event: wx.Event) -> None:
        self._functions.remove_category()
        
    def _on_remove_entry(self, event: wx.Event) -> None:
        self._functions.remove_entry()
    
    def _on_rename_category(self, event: wx.Event) -> None:
        self._functions.rename_category()
    
    def _on_clear_category(self, event: wx.Event) -> None:
        self._functions.clear_category()
    
    def _on_save_datafile_as(self, event: wx.Event) -> None:
        self._functions.save_datafile_as()
    
    def _on_show_datafile_in_folder(self, event: wx.Event) -> None:
        self._functions.show_datafile_in_folder()
    
    def _on_copy_datafile_path(self, event: wx.Event) -> None:
        self._functions.copy_datafile_path()
    
    def _on_change_datafile_directory(self, event: wx.Event) -> None:
        self._functions.change_datafile_dir()
    
    def _on_load_from_datafile(self, event: wx.Event) -> None:
        self._functions.load_data_from_file()
    
    def _on_create_backup(self, event: wx.Event) -> None:
        self._functions.create_backup()
    
    def _on_change_file_password(self, event: wx.Event) -> None:
        self._functions.change_password()
    
    def _on_restore_from_backup(self, event: wx.Event) -> None:
        self._functions.restore_from_backup()

   
    
    #  Edit funcs --------------------------------------------
    
    def _update_moving_entity(self):
        self._moving_entity = not self._moving_entity
    
    def _on_copy_password(self, event: wx.Event) -> None:
        self._functions.copy_password()
        
    def _on_copy_username(self, event: wx.Event) -> None:
        self._functions.copy_username()
    
    def _on_copy_url(self, event: wx.Event) -> None:
        self._functions.copy_url()
    
    def _on_undo(self, event: wx.Event) -> None:
        self._functions.undo()
    
    def _on_redo(self, event: wx.Event) -> None:
        self._functions.redu()
    
    def _on_move_entry_to(self, event: wx.Event):
        event_id = event.GetId()
        category = self._id_category[event_id]
        self._functions.move_entry_to_category(category=category)
    
    def _on_move_category_up(self, event: wx.Event | None = None) -> None:
        if not self._moving_entity:
            self._update_moving_entity()
            self._functions.move_category_up()
            wx.CallLater(200, self._update_moving_entity)
        else:
            wx.CallLater(100, self._on_move_category_up)
            
    def _on_move_category_down(self, event: wx.Event | None = None) -> None:
        if not self._moving_entity:
            self._update_moving_entity()
            self._functions.move_category_down()
            wx.CallLater(200, self._update_moving_entity)
        else:
            wx.CallLater(100, self._on_move_category_down)
        
    def _on_move_entry_up(self, event: wx.Event | None = None) -> None:
        if not self._moving_entity:
            self._update_moving_entity()
            self._functions.move_entry_up()
            wx.CallLater(200, self._update_moving_entity)
    
    def _on_move_entry_down(self, event: wx.Event | None = None) -> None:
        if not self._moving_entity:
            self._update_moving_entity()
            self._functions.move_entry_down()
            wx.CallLater(200, self._update_moving_entity)
    
    
    #  File Encryption funcs --------------------------------------------

    def _on_file_encryption(self, event: wx.Event) -> None:
        self._functions.file_encryption()
    
    # def _on_file_decrypt(self, event: wx.Event) -> None:
    #     self._functions.file_encryption()
        
    
    #  Help funcs --------------------------------------------
  
    def _on_help(self, event: wx.Event) -> None:
        self._functions.help()
        