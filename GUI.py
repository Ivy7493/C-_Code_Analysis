import PySimpleGUI as sg
import os.path
from ProcessController import ProcessController as PrscC

file_list_column = [
    [
        sg.Text("Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]

header_viewer_column= [
    [sg.Text("Once you have selected a source folder, please press OK")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Listbox([],size=(50,25),key="listHeaders")],    
    [sg.Button("OK")],
]

source_viewer_column=[
    [sg.Listbox([],size=(50,25),key="listSources")],
]

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(header_viewer_column),
        sg.VSeparator(),
        sg.Column(source_viewer_column)
    ]
]

window = sg.Window("Student code analyser", layout)
window.set_min_size
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        print(type(folder))
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".cpp", ".h"))
        ]
        window["-FILE LIST-"].update(fnames)
    if event == "OK":
        headers,sources = PrscC(os.path.join(folder))
        window["listHeaders"].Update(headers.keys())
        window["listSources"].Update(sources.keys())
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        print("butts")
        
window.close()