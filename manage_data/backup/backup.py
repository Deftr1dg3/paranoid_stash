#!/usr/bin/env python3

import os
from datetime import datetime
from hashlib import sha256


class BackUp:
    
    _BACKUP_DIR_PATH = settings.BACKUP_PATH
    _CONTROL_HASH_PATH = BackupConst.CONTROL_HASH_PATH
    
    def __init__(self) -> None:
        self._hash_file = self._control_hash_path()
        self._backup_dir = self._backup_dir_path()
        
        self._control_backups_ammount()
    
    def _backup_dir_path(self) -> str:
        if not os.path.exists(self._BACKUP_DIR_PATH):
            os.makedirs(self._BACKUP_DIR_PATH)
        return self._BACKUP_DIR_PATH
        
    def _control_hash_path(self) -> str:
        if not os.path.exists(self._CONTROL_HASH_PATH):
            dirname = os.path.dirname(self._CONTROL_HASH_PATH)
            os.makedirs(dirname, exist_ok=True)
            with open(self._CONTROL_HASH_PATH, "w", encoding=GeneralConst.ENCODING_FORMAT) as f:
                ...
        return self._CONTROL_HASH_PATH
        
    def _create_backup_file_name(self) -> str:
        current_datetime = datetime.now()
        file_name = current_datetime.strftime(BackupConst.BACKUP_FILE_NAME_FORMAT) + GeneralConst.DATAFILE_EXTENSION
        return file_name

    def _create_control_hash(self, json_data: str) -> str:
        data_hash = sha256(json_data.encode(GeneralConst.ENCODING_FORMAT)).hexdigest()
        return data_hash

    def _get_control_hash(self) -> str:
        with open(self._hash_file, "r") as f:
            control_hash = f.read()
        return control_hash
    
    def _made_changes(self, json_data: str) -> bool:
        self._new_hash = self._create_control_hash(json_data)
        current_hash = self._get_control_hash()
        if not self._new_hash == current_hash:
            return True
        return False
    
    def _backup_data(self, b64_data: str) -> None:
        file_name = self._create_backup_file_name()
        file_path = self._backup_dir + os.sep + file_name 
        with open(file_path, "w", encoding=GeneralConst.ENCODING_FORMAT) as f:
            f.write(b64_data)
        with open(self._hash_file, "w", encoding=GeneralConst.ENCODING_FORMAT) as f:
            f.write(self._new_hash)
            
    def _get_backups_list(self) -> list[str]:
        backups = os.listdir(self._backup_dir)
        backups_abspath = [self._backup_dir + os.sep + file for file in backups]
        sorted_backups = sorted(backups_abspath, key=os.path.getctime, reverse=True)
        return sorted_backups
    
    def _remove_old_backups(self, sorted_backups: list[str]) -> list[str]:
        if len(sorted_backups) > BackupConst.STORED_BACKUPS:
            for file in sorted_backups[BackupConst.STORED_BACKUPS:]:
                if os.path.isfile(file):
                    os.remove(file)
            return sorted_backups[:BackupConst.STORED_BACKUPS]
        return sorted_backups[:BackupConst.STORED_BACKUPS]
                
    def _control_backups_ammount(self) -> None:
        sorted_backups = self._get_backups_list()
        available_backups = self._remove_old_backups(sorted_backups)
        
    def save_backup_file(self, json_data: str, b64_data: str) -> None:
        if self._made_changes(json_data):
            self._backup_data(b64_data)
            return 
        if not self._get_backups_list():
            self._backup_data(b64_data)
            return
            
   