
# -*- coding: utf-8 -*-

import os
import shutil
import img2pdf
import natsort
import glob
import PIL.Image
import PySimpleGUI as sg

pwd = os.getcwd()
used = os.path.join(pwd, "used")


def filename():
    sg.theme('DefaultNoMoreNagging')

    layout = [[sg.Text('Enter file name')],
              [sg.InputText()],
              [sg.Submit(), sg.Cancel()]]

    window = sg.Window('Image2PDF', layout)

    event, values = window.read()
    window.close()
    if event == 'Submit':
        return str(values[0])
    else:
        return 'none'


def img_files_exists():
    for files in os.listdir():
        if files.endswith((".jpg", ".png", ".jpeg")):
            return True


def fix_exif_orientation():
    # Fix Exif orientation
    os.makedirs("used", exist_ok=True)
    os.makedirs("fixed", exist_ok=True)

    for files in os.listdir():
        if files.endswith((".jpg", ".png", ".jpeg")):
            image = PIL.Image.open(files)
            image.save(os.path.join(pwd, "fixed", files))
            # print("Saved to fixed")
            shutil.move(files, "used")
            # print("Moved to used")


def create_pdf():
    os.chdir("fixed")

    with open(f_name, "wb") as f:
        f.write(img2pdf.convert([i for i in natsort.natsorted(os.listdir()) if i.endswith((".png", ".jpg", ".jpeg"))]))
        # Here you can add extensions


def rm_fixed():
    # Remove "Fixed" Files

    for a in os.listdir(os.path.join(pwd, "fixed", "")):
        if a.endswith((".jpg", ".png")):
            os.remove(os.path.join(pwd, "fixed", a))

    for gl in glob.glob("*.pdf"):
        shutil.move(gl, pwd)

    os.chdir(pwd)


# reuse..
are_files = img_files_exists()


if are_files is True:
    f_name = filename() + ".pdf"
    if f_name != "none.pdf":
        # print(f_name)
        fix_exif_orientation()
        create_pdf()
        rm_fixed()
        sg.SystemTray.notify('Image2PDF', 'PDF file created')

    if f_name == "none.pdf":
        sg.SystemTray.notify('Image2PDF', 'Provide file name, exit now!')

if are_files is not True:
    sg.SystemTray.notify('Image2PDF', 'Put images to catalog!!')

