#!/usr/bin/python3

import PySimpleGUI as sg

print = sg.EasyPrint

layout = [[sg.Text('(Les numéros de pièces seront ajoutés automatiquement. Mettre uniquement "Pièce n°" en 3e ligne.):')],
            [sg.Text('Dossier des fichiers pdfs à tamponner (dont les noms commencent par 001, 002, ..)', size=(35, 2)), sg.InputText(), sg.FolderBrowse()],
            [sg.Text('Dossier dans lequel les pdfs tamponnés seront enregistrés:', size=(35, 2)), sg.InputText(), sg.FolderBrowse()],
            [sg.Text('1ère ligne du tampon:', size=(35, 2)), sg.InputText()],
            [sg.Text('2ème ligne du tampon:', size=(35, 2)), sg.InputText()],
            [sg.Text('3ème ligne du tampon ("Pièce n.")', size=(35, 2)), sg.InputText()],
            [sg.Checkbox('Tamponner chaque page du fichier? (Seulement la 1ère page par défaut)', size=(65,2), default=False)],
            [sg.Submit(), sg.Cancel()]]


import fitz
import shutil
from os import listdir
from os.path import isdir, isfile, join


window = sg.Window('Inputs', layout)

event, value_list = window.Read()
input_path = value_list[0]
output_path = value_list[1]
line_one = value_list[2]
line_two = value_list[3]
line_three = value_list[4]
stampall = value_list[5]
maxstring = max((len(line_one)), (len(line_two)),(len(line_three) + 4))
leftwidth = maxstring*7+26

from fitz.utils import getColor

yellow  = getColor("darkgoldenrod")
black   = getColor("black")
white   = getColor("white")
red     = getColor("red")
wood    = getColor("wheat2")
wood2 = getColor("wheat3")

print("Tamponner toutes le pages:", stampall)
print("Char. max.:", maxstring)

# stamps_path = input()

#print("\n Enter the full path to the OUTPUT folder:")

#output_path = input()

print("Dossier des fichiers à tamponner: ", input_path, '\n' \
        #"Stamps file/folder: ", stamps_path, '\n' \
        "Dossier des fichiers tamponnées: ", output_path, '\n')

input_files = [f for f in listdir(input_path) if isfile(join(input_path, f))]

print("Fichiers à tamponner: ", input_files, '\n')


for i in input_files:

    doc = fitz.open(f"{input_path}/{i}")

    text = [f"{line_one}", f"{line_two}", f"{line_three} {i[:3]}"]

    if stampall == True:

        for page in doc:

            r1 = fitz.Rect(page.rect.width - leftwidth, page.rect.height - 65, page.rect.width - 25, page.rect.height - 20) # directly define rectangle using page.rect

            # p2 = fitz.Point(page.rect.width - 25, page.rect.height - 25)

            page.drawRect(r1, color=black, fill=white, overlay=True) # Draw first to give properties

            rc = page.insertTextbox(r1, text, color = black, align=1, fontname="Courier", border_width=2)

        doc.save(f"{i}")

    else:

        page = doc[0]

        text = [f"{line_one}", f"{line_two}", f"{line_three} {i[:3]}"]

            #r1 = fitz.Rect(400,750,550,800)   # rectangle (x0, y0, x1, y1) in pixels, bottom right For upper right try fitz.Rect(450,20,550,120)

        r1 = fitz.Rect(page.rect.width - leftwidth, page.rect.height - 65, page.rect.width - 25, page.rect.height - 20)

            # p2 = fitz.Point(page.rect.width - 25, page.rect.height - 25)

        page.drawRect(r1, color=black, fill=white, overlay=True) # Draw first to give properties

        rc = page.insertTextbox(r1, text, color = black, align=1, fontname="Courier", border_width=2) #Default : align=TEXT_ALIGN_LEFT (0) ; border_width=1 TEXT_ALIGN_CENTER

    doc.save(f"{i}")

# Check usage for doc.name Runtime error: cannot open file 'stamped-/home/xxx/xxx/Original.pdf': No such file or directory


output_files = [f for f in listdir(".") if isfile(join(".", f))]
print("Fichiers tamponnés:")
for f in output_files:
    if f[-3:] == "pdf":
        print(f)

def output(output_path):
    for f in output_files:
        if f[-3:] == "pdf":
            shutil.move(f, output_path)

output(output_path)

while True:
    event, values = window.Read()
    if event is None or event == 'Cancel':
        break




