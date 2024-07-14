#!/usr/bin/env python3


import wx

app = wx.App(False)  # Create a new application

frame = wx.Frame(None, wx.ID_ANY, "Image Viewer", size=(400, 300))  # Create a frame (window)
panel = wx.Panel(frame)  # Create a panel in the frame

file_path = 'cat_with_guitar.jpg'
# Load the image
image = wx.Image(file_path, wx.BITMAP_TYPE_JPEG)

# Convert the image to a bitmap
bitmap = wx.StaticBitmap(panel, -1, wx.Bitmap(image))

# Set up the layout with a box sizer
sizer = wx.BoxSizer(wx.VERTICAL)
sizer.Add(bitmap, 0, wx.ALL | wx.CENTER, 5)

panel.SetSizer(sizer)

frame.Show(True)  # Show the frame
frame.Raise()  # Bring the frame to the front

app.MainLoop()  # Start the event loop
