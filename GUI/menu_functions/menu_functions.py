from __future__ import annotations

import os
import time
import threading
import pyperclip
import platform
import subprocess
from pathlib import Path 

import logging

from GUI.menu_functions.select_color_theme import SelectColorThemeFrame
from GUI.modals.popups import dialog_popup, get_input, message_popup, save_file_as, select_dir, select_file
from GUI.base_panel import BasePanel
from GUI.modals.set_new_password import SetNewPasswordFrame
from GUI.modals.copy_popup import CopyPopup
from GUI.modals.get_password_from_user import GetPasswordFrame

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from GUI.base_panel import BasePanel
    

lock = threading.Lock()  
logging.basicConfig(filename='app.log', level=logging.DEBUG)



class MenuFunctions():
    
    _instance: Optional['MenuFunctions'] = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            inst = super().__new__(cls)
            cls._instance = inst 
        return cls._instance
    
    def __init__(self, base_panel: BasePanel) -> None:

        self._base_panel = base_panel
        
        self._config = self.settings['menu']
        
        self._color_panel_active = False
    
    @property
    def settings(self):
        return self._base_panel.settings
    
    @property
    def manage_data(self):
        return self._base_panel._manage_data
    
    # Move --------------------------------------------------------   
    
    def move_category_up(self) -> None:
        self.manage_data.move_category()
        self._base_panel.refresh_left_panel()
        time.sleep(0.05)

    def move_category_down(self) -> None:
        self.manage_data.move_category(direction=1)
        self._base_panel.refresh_left_panel()
        time.sleep(0.05)
    
    def move_entry_up(self) -> None:
        if self.manage_data.search_results is None:
            self.manage_data.move_entry()
            self._base_panel.refresh_mid_panel()
            time.sleep(0.05)

    def move_entry_down(self) -> None:
        if self.manage_data.search_results is None:
            self.manage_data.move_entry(direction=1)
            self._base_panel.refresh_mid_panel()
            time.sleep(0.05)
       
    # Move --------------------------------------------------------   
         
    # Copy --------------------------------------------------------
    
    def copy_record_name(self) -> None:
        if self._base_panel.selected_entry_inst is None:
            return
        self._base_panel.selected_entry_inst.copy_record_name()
        
    def copy_password(self) -> None:
        if self._base_panel.selected_entry_inst is None:
            return
        self._base_panel.selected_entry_inst.copy_password()
        
    def copy_username(self) -> None:
        if self._base_panel.selected_entry_inst is None:
            return
        self._base_panel.selected_entry_inst.copy_username()
    
    def copy_url(self) -> None:
        if self._base_panel.selected_entry_inst is None:
            return
        self._base_panel.selected_entry_inst.copy_url()
        
    # Copy --------------------------------------------------------
    
    # Category ------------------------------------------------------
    
    def _name_is_valid(self, new_category):
        return not (new_category in self._base_panel._manage_data.data)
    
    def add_category(self) -> None:
        color = self._base_panel._color_themes[self._base_panel._current_theme]['medium']
        new_category = get_input(color=color, hint="Enter desired category name:", title="New Category")
        if new_category is None or new_category == "":
            return 
        if self._name_is_valid(new_category):
            self.manage_data.add_category(new_category)
            self.manage_data.selected_entry = None
            self.manage_data.search_results = None
            self._base_panel.refresh_body_panel()
        else:
            message_popup(message="Category with this name alrady exists.", title="INVALID !")
    
    def rename_category(self) -> None:
        if self._base_panel._manage_data.selected_category is None:
            return
        color = self._base_panel._color_themes[self._base_panel._current_theme]['medium']
        new_category = get_input(color=color, hint="Enter desired category name:", title="New Category")
        if new_category is None or new_category == "":
            return 
        self.manage_data.rename_category(new_category)
        self._base_panel.refresh_body_panel()
        
    def remove_category(self) -> None:
        if self._base_panel._manage_data.selected_category is None:
            return
        message = self._config['category']['remove_dialog']['message']
        title = self._config['category']['remove_dialog']['title']
        confirmed = dialog_popup(message=message, title=title)
        if confirmed:
            self.manage_data.delete_category()
            self._base_panel.refresh_body_panel()
    
    def clear_category(self) -> None:
        if self._base_panel._manage_data.selected_category is None:
            return
        message = self._config['category']['clear_dialog']['message']
        title = self._config['category']['clear_dialog']['title']
        confirmed = dialog_popup(message=message, title=title)
        if confirmed:
            self.manage_data.clear_category()
            self._base_panel.refresh_body_panel()
            
    # Category ------------------------------------------------------
    
    # Entry ------------------------------------------------------
    
    def add_entry(self) -> None:
        if self.manage_data.search_results is None:
            self.manage_data.add_entry()
            self._base_panel.refresh_mid_panel()
            self._base_panel.refresh_right_panel()
        
    def remove_entry(self) -> None:
        if self.manage_data.selected_entry is None:
            return
        message = self._config['entry']['remove_dialog']['message']
        title = self._config['entry']['remove_dialog']['title']
        confirmed = dialog_popup(message=message, title=title)
        if confirmed:
            self.manage_data.delete_entry()

            if self.manage_data.search_results is not None:
                query = self._base_panel.top_panel.top_mid_panel.get_query()
                self.manage_data.search(query)
            
            BasePanel.set_selected_entry(None)
            self._base_panel.refresh_mid_panel()
            self._base_panel.refresh_right_panel()
    
    def move_entry_to_category(self, category: str):
        if self.manage_data.move_entry_to_category(category=category):
            BasePanel.set_selected_entry(None)
            self._base_panel.refresh_body_panel()
            message_popup(f"Entry moved to {category} successfully.", "Info.")
    
    
    # Entry ------------------------------------------------------
    
    # State ------------------------------------------------------
    
    def undo(self) -> None:
        if self.manage_data.backward():
            self._base_panel.refresh_body_panel()
            self._base_panel.body.right_panel.deselect_all()
    
    def redu(self) -> None:
        if self.manage_data.forward():
            self._base_panel.refresh_body_panel() 
            self._base_panel.body.right_panel.deselect_all()
    
    # State ------------------------------------------------------
    
    # Search ------------------------------------------------------
    
    def search(self) -> None:
        query = self._base_panel.top_panel.top_mid_panel.get_query()
        self.manage_data.search(query)
        self.manage_data.selected_category = None 
        self.manage_data.selected_entry = None 
        BasePanel.set_selected_entry(None)
        self._base_panel.refresh_body_panel()

    
    # Search ------------------------------------------------------
    
    # State ------------------------------------------------------
    

    def choose_color_theme(self) -> None:
        if not self._color_panel_active:
            self._color_panel_active = True
            self.frame = SelectColorThemeFrame(self._base_panel, self.settings, self._base_panel._color_themes)
            self.frame.Show()
        else:
            try:
                self.frame.Raise()
            except RuntimeError:
                self._color_panel_active = False 
                self.choose_color_theme()
    
    def change_password(self) -> None:
        set_new_password = SetNewPasswordFrame(self._base_panel, self.manage_data._df, self.settings, self._base_panel._color_themes, self._base_panel._current_theme, change_password=True)
        set_new_password.Show()
    

    # State ------------------------------------------------------
    
    # Datafile ------------------------------------------------------
    
    def save_datafile_as(self) -> None:
        save_as = save_file_as(self._config['default_datafile_name'])
        if save_as is not None:
            save_as = Path(save_as)
            datafile_path: Path = self.manage_data._df.io.file_path
            if save_as.exists():
                confirmed = dialog_popup(f"Aru you sure you want to replace it?", "File Already Exist")
                if confirmed:
                    with open(datafile_path, "r", encoding="utf-8") as f:
                        data = f.read()
                    with open(save_as, "w", encoding="utf-8") as f:
                        f.write(data)
                    message_popup(self._config['save_message']['message'].format(save_as), self._config['save_message']['title'])
            else:
                with open(datafile_path, "r", encoding="utf-8") as f:
                        data = f.read()
                with open(save_as, "w", encoding="utf-8") as f:
                    f.write(data)
                message_popup(self._config['save_message']['message'].format(save_as), self._config['save_message']['title'])
            
    def show_datafile_in_folder(self) -> None:
        datafile_path: Path = self.manage_data._df.io.file_path
        
        if platform.system() == 'Windows':
            subprocess.run(['explorer', '/select,', datafile_path])
        elif platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', '-R', datafile_path])
        else: 
            subprocess.run(['xdg-open', os.path.dirname(datafile_path)])
    
    def copy_datafile_path(self) -> None:
        datafile_path = str(self.manage_data._df.io.file_path.resolve())    
        pyperclip.copy(datafile_path)   
        copy_indicator = CopyPopup(self._base_panel) 
        copy_indicator.Show()    
    
    
    def change_datafile_dir(self) -> None:
        datafile_path: Path = self.manage_data._df.io.file_path
        file_name = datafile_path.name 
        new_directory = select_dir()
        if new_directory is not None:
            new_path = Path(new_directory) / str(file_name)
            if new_path.exists():
                confirmed = dialog_popup(f"Aru you sure you want to replace it?", "File Already Exist")
                if confirmed:
                    self.manage_data._df.io.file_path = str(new_path) 
                    self.manage_data.update()
                return
            
            self.manage_data._df.io.file_path = str(new_path) 
            self.manage_data.update()
    
    # def change_datafile(self) -> None:
    #     self._current_file = str(self.manage_data._df.io.file_path)
    #     self._current_password = self.manage_data._df.password 
    #     new_datafile = select_file()
    #     if new_datafile is not None:
    #         self.manage_data._df.io.file_path = new_datafile
    #         get_password = GetPasswordFrame(self.manage_data._df, self.settings, self._base_panel._color_themes, self._base_panel._current_theme, self)
    #         get_password.Show()
    
    # def restore_df(self):
    #     self.manage_data._df.io.file_path = self._current_file
    #     self.manage_data._df.password = self._current_password
    
    # def LaunchMainApp(self) -> None:
    #     self._base_panel.refresh_body_panel()
    
    def restore_from_backup(self) -> None:
        current_file = str(self.manage_data._df.io.file_path)
        backups_dir = self.settings['global']['backups']
        restore_from = select_file(dir=backups_dir, title="Select Backup File")
        if restore_from is not None:
            self.manage_data._df.backup()
            try:
                self.manage_data._df.load_data(restore_from)
            except ValueError:
                message_popup(message=self.settings['get_password']['wrong_password']['message'], title=self.settings['get_password']['wrong_password']['title'])
            else:
                self._base_panel.refresh_body_panel()
            
            
                
            