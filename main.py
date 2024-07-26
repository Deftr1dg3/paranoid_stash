#!/usr/bin/env python3
import os 
import sys
import wx 
import json
from pathlib import Path

from GUI import GUIApp, MainFrame
from manage_data import ManageData, DataFile

SETTINGS_PATH = Path('./settings.json')

with open(SETTINGS_PATH, 'r') as f:
    settings = json.load(f)

print("WORKED TILL HERE", flush=True)
df = DataFile(settings['data'])
print("WORKED TILL HERE", flush=True)
df.password = '1234'


# df.create_new_data_file()

print("WORKED TILL HERE")

try:
    df.load_data()
except Exception as ex:
    print(f'Unable to decrypt file -> {ex}')
else:
    print("ELSO")
    
print("WORKED TILL HERE END")

md = ManageData(df)

try:
    app = wx.App()
    f = MainFrame(md, settings['color_theme'])
    f.Show()
    app.MainLoop()
except Exception as ex:
    print(f'EXCEPTION IN MAIN ==> {ex}')
except BaseException as ex:
    print(f'BASE EXCEPTION IN MAIN ==> {ex}')
    
    
# app = GUIApp(settings)
# app.MainLoop()

