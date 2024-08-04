#!/usr/bin/env python3

import os
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from GUI.modals.popups import message_popup

# import logging

# log_format = '%(asctime)s - %(levelname)s - %(message)s'
# logging.basicConfig(filename="app.log", level=logging.INFO, format=log_format)

class BackUp:
    
    def __init__(self, settings: dict) -> None:
        
        self._settings = settings
        
        self._hash_file = self._validate_control_hash_path(Path(settings['control_hash']))
        self._backup_dir = self._validate_backup_dir_path(Path(settings['backups']))
        
        # self._available_backups = self._control_backups_ammount()
        
        self._new_hash: str
        
    
    def _validate_backup_dir_path(self, backup_path: Path) -> Path:
        if not backup_path.exists():
            backup_path.mkdir(parents=True, exist_ok=True)
        try:
            return backup_path.relative_to(Path.cwd())
        except ValueError:
            return Path(os.path.relpath(backup_path, Path.cwd()))
        
    def _validate_control_hash_path(self, hash_path: Path) -> Path:
        path = hash_path.parent 
        if not hash_path.exists():
            path.mkdir(parents=True, exist_ok=True)
            hash_path.touch(exist_ok=True)
        try:
            return hash_path.relative_to(Path.cwd())
        except ValueError:
            return Path(os.path.relpath(hash_path, Path.cwd()))
        
    def _create_backup_file_name(self) -> str:
        current_datetime = datetime.now()
        file_name = current_datetime.strftime(self._settings['backup_file_name_format']) + self._settings['extension']
        return file_name

    def _create_control_hash(self, json_data: str) -> str:
        data_hash = sha256(json_data.encode('utf-8')).hexdigest()
        return data_hash

    def _get_control_hash(self) -> str:
        with open(self._hash_file, "r", encoding=self._settings['encoding']) as f:
            control_hash = f.read()
        return control_hash
    
    def _made_changes(self, json_data: str) -> bool:
        self._new_hash = self._create_control_hash(json_data)
        current_hash = self._get_control_hash()
        if not self._new_hash == current_hash:
            return True
        return False
    
    def _backup_data(self, b64_data: str) -> str | None:
        file_name = self._create_backup_file_name()
        file_path = self._backup_dir / file_name 
        try:
            with open(file_path, "w", encoding=self._settings['encoding']) as f:
                f.write(b64_data)
            with open(self._hash_file, "w", encoding=self._settings['encoding']) as f:
                f.write(self._new_hash)
        except Exception as ex:
            # logging.error(f"Unable to save backup due to Exception:\n{ex}")
            message_popup(message=f"Unable to save backup due to Exception:\n{ex}", title="Error.")
        else:
            return file_name
            
    def _get_backups_list(self) -> list[Path]:
        backups = os.listdir(self._backup_dir)
        backups_abspath = [self._backup_dir / file for file in backups]
        sorted_backups = sorted(backups_abspath, key=os.path.getctime, reverse=True)
        return sorted_backups
    
    def _remove_old_backups(self, sorted_backups: list[Path]) -> list[Path]:
        if len(sorted_backups) > self._settings['max_backups']:
            for file in sorted_backups[self._settings['max_backups']:]:
                if os.path.isfile(file):
                    os.remove(file)
        return sorted_backups[:self._settings['max_backups']]
                
    def _control_backups_ammount(self) -> list[Path]:
        sorted_backups = self._get_backups_list()
        available_backups = self._remove_old_backups(sorted_backups)
        return available_backups
        
    def save_backup_file(self, json_data: str, b64_data: str) -> str | None:
        if self._made_changes(json_data):
            created = self._backup_data(b64_data)
            self._control_backups_ammount()
            return created
        return "already exists"
   