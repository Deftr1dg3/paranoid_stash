from __future__ import annotations
import time

from GUI.menu_functions.select_color_theme import SelectColorThemeFrame
from GUI.modals.popups import dialog_popup, get_input, message_popup
from GUI.base_panel import BasePanel

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from GUI.base_panel import BasePanel

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
    
    def add_category(self):
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
    
    def add_entry(self):
        self.manage_data.add_entry()
        self._base_panel.refresh_mid_panel()
        self._base_panel.refresh_right_panel()
        
    def remove_entry(self):
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
    
    
    # Entry ------------------------------------------------------
    
    # State ------------------------------------------------------
    
    def undo(self):
        if self.manage_data.backward():
            self._base_panel.refresh_body_panel()
            self._base_panel.body.right_panel.deselect_all()
    
    def redu(self):
        if self.manage_data.forward():
            self._base_panel.refresh_body_panel() 
            self._base_panel.body.right_panel.deselect_all()
    
    # State ------------------------------------------------------
    
    # State ------------------------------------------------------
    
    def search(self):
        query = self._base_panel.top_panel.top_mid_panel.get_query()
        self.manage_data.search(query)
        self.manage_data.search(query)
        self.manage_data.selected_category = None 
        self.manage_data.selected_entry = None 
        BasePanel.set_selected_entry(None)
        self._base_panel.refresh_body_panel()
        
    def choose_color_theme(self):
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
    
    
