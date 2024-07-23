#!/usr/bin/env python3
import os 
import sys
import wx 
import json
from pathlib import Path

from GUI import MainFrame
from manage_data import ManageData, DataFile

SETTINGS_PATH = Path('./settings.json')

with open(SETTINGS_PATH, 'r') as f:
    settings = json.load(f)

df = DataFile(settings['data'])
df.password = 'hello'

# df.create_new_data_file()

try:
    df.load_data()
except ValueError:
    print('Unable to decrypt file')
    os._exit(0)

md = ManageData(df)


# md.selected_category = 'Internet'
# md.add_entry()

# print(md)

try:
    app = wx.App()
    f = MainFrame(md, settings['color_theme'])
    f.Show()
    app.MainLoop()
except Exception as ex:
    print(f'EXCEPTION ==> {ex}')
except BaseException as ex:
    print(f'BASE ==> {ex}')

