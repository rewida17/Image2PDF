
# -*- coding: utf-8 -*-

import os
import shutil
import img2pdf
import natsort
import glob
import wx
import PIL.Image


# Fix Exif orientation 
os.makedirs("used", exist_ok=True)
os.makedirs("fixed", exist_ok=True)

pwd = os.getcwd()
used = os.path.join(pwd, "used")


for files in os.listdir():
    if files.endswith((".jpg", ".png")):
        image = PIL.Image.open(files)
        image.save(os.path.join(pwd, "fixed", files))
        #print("Saved to fixed")
        shutil.move(files, "used")
      #  print("Moved to used")

# Fix Exif

##UI
app = wx.App()

frame = wx.Frame(None, -1)
frame.SetSize(0, 0, 200, 50)

# Create text input
dlg = wx.TextEntryDialog(frame, 'File name:', 'IMG2PDF')
if dlg.ShowModal() == wx.ID_OK:
    dlg.Destroy()
##UI



#File name
fname = dlg.GetValue() + ".pdf"

#Create PDF

os.chdir("fixed")

with open(fname, "wb") as f:
    f.write(img2pdf.convert([i for i in natsort.natsorted(os.listdir()) if i.endswith((".png", ".jpg"))]))  #Here you can add extensions 

#os.chdir(pwd)

#Remove "Fixed" Files


for a in os.listdir(os.path.join(pwd, "fixed", "")):
    if a.endswith((".jpg", ".png")):
        os.remove(os.path.join(pwd, "fixed", a))

for gl in glob.glob("*.pdf"):
   shutil.move(gl , pwd)

os.chdir(pwd)
#print(os.getcwd())
