#!/usr/bin/env python3
import os 
import sys
import wx 
import json

from GUI import MainFrame
from manage_data import ManageData, DataFile

SETTINGS_PATH = './settings.json'

with open(SETTINGS_PATH, 'r') as f:
    settings = json.load(f)

df = DataFile(settings)
df.password = 'hello'
try:
    df.load_data()
except ValueError:
    print('Unable to decrypt file')
    os._exit(0)

md = ManageData(df)

# print(md)


app = wx.App()
f = MainFrame(md, settings['color_theme'])
f.Show()
app.MainLoop()
