#/Library/Frameworks/Python.framework/Versions/3.12/bin/python3

import sys
import json
from pathlib import Path

from GUI import GUIApp

# import logging

# log_format = format='%(asctime)s - %(levelname)s - %(message)s'
# logging.basicConfig(
#     filename='app.log', 
#     level=logging.DEBUG, 
#     format=log_format
# )


SETTINGS_PATH = Path('settings/settings.json')
GUI_SETTINGS_PATH = Path('settings/gui_settings.json')
COLOR_THEMES_PATH = Path('settings/color_themes.json')


def _load_configs() -> tuple[dict, dict, dict]:
    try:
        with open(SETTINGS_PATH, 'r') as f:
            settings = json.load(f)
    except Exception as ex:
        raise 
    
    try:
        with open(GUI_SETTINGS_PATH, 'r') as f:
            gui_settings = json.load(f)
    except Exception as ex:
         raise
    
    try:
        with open(COLOR_THEMES_PATH, 'r') as f:
            color_themes = json.load(f)
    except Exception as ex:
         raise
        
    return settings, gui_settings, color_themes
    
    
def main():
    try:
        settings, gui_settings, color_themes = _load_configs()
    except Exception as ex:
        # logging.error(f"Exception: {ex}")
        sys.exit(1)
    
    try: 
        app = GUIApp(settings=settings, gui_settinghs=gui_settings, color_themes=color_themes)
        app.MainLoop()
    except Exception as ex:
        # logging.error(f"Exception: {ex}")
        sys.exit(1)
        
    
if __name__ == '__main__': 
    try: 
        main()
    except Exception as ex:
        print(f"EXCEPTION: {ex}")



