#!/usr/bin/env python3

import wx
import json 
from pathlib import Path


# SETTINGS_PATH = './GUI/gui_settings.json'

# with open(SETTINGS_PATH, 'r') as f:
#     SETTINGS = json.load(f)

    

def get_input(color: str, hint: str = "", title: str = "", default_value: str = "", parent: (wx.Panel | None) = None) -> (str | None):
    user_input = None
    dlg = wx.TextEntryDialog(parent, hint, title, default_value)
    dlg.SetMinSize(dlg.GetSize())
    dlg.SetMaxSize(dlg.GetSize())
    dlg.SetBackgroundColour(wx.Colour(color))
    if dlg.ShowModal() == wx.ID_OK:
        user_input = dlg.GetValue()
    dlg.Destroy()
    return user_input


def message_popup(message: str = "", title: str = "", parent: (wx.Panel | None) = None) -> None:
        dlg = wx.MessageDialog(parent, message, title, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        
        
def dialog_popup(message: str = "", title: str = "", yes_default=False, parent: (wx.Panel | None) = None) -> bool:
    if yes_default:
        dialog = wx.MessageDialog(None, message, title, wx.YES_NO | wx.ICON_QUESTION | wx.YES_DEFAULT)
    else:
        dialog = wx.MessageDialog(None, message, title, wx.YES_NO | wx.ICON_QUESTION | wx.NO_DEFAULT)
    result = dialog.ShowModal()
    dialog.Destroy()
    if result == wx.ID_YES:
        return True
    return False


def select_file(dir: str, title: str = "Selecet File", wildcard: str = "*.*") -> (str | None):
    
    file_dialog = wx.FileDialog(None, 
                            title, 
                            wildcard=wildcard, 
                            style=wx.FD_OPEN,
                            defaultDir=dir)
    if file_dialog.ShowModal() == wx.ID_OK:
        file_path = file_dialog.GetPath()
        file_dialog.Destroy()
        return file_path
    file_dialog.Destroy()
    
    
def save_file_as(dir: str, file_name: str, title: str = "Save File as...") -> (str | None):
    file_dialog = wx.FileDialog(None,
                            title, 
                            defaultFile=file_name, 
                            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
                            defaultDir=dir)
    if file_dialog.ShowModal() == wx.ID_OK:
        save_path = file_dialog.GetPath()
        file_dialog.Destroy()
        return save_path
    file_dialog.Destroy()


def select_dir(dir: str, title: str = "Select Directory") -> (str | None):
    dir_dialog = wx.DirDialog(None, title)
    if dir_dialog.ShowModal() == wx.ID_OK:
        dir_path = dir_dialog.GetPath()
        dir_dialog.Destroy()
        return dir_path
    dir_dialog.Destroy()


