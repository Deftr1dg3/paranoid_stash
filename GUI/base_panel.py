import wx


class BasePanel(wx.Panel):
    _instances = []
    def __new__(cls, *args, **kwargs):
        i = super().__new__(cls, *args, **kwargs)
        cls._instances.append(i)
        return i
        
    def applay_color_theme(self, theme_name: str):
        raise NotImplementedError

