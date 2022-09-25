import PySimpleGUI as sg
import os.path
import textwrap
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
    [sg.Button("OK"),
     sg.Button("VIEW",key = "viewButton",visible = False)],
]

source_viewer_column=[
    [sg.Listbox([],size=(50,25),key="listSources")],
]

report_viewer_column = [
    [sg.Text("Your File had the following issues:")],
    [sg.Text(size = (40,1))],
    [
        sg.Text("Instances of Implementation Inheritance:"),
        sg.Text("",key = "impText"),
    ],    
    [sg.Text("Location(s):")],
    [sg.Text("",key = "impLocText")],
    [
        sg.Text("Instances of Global Variables:"),
        sg.Text("",key = "globText"),
    ],
    [sg.Text("Location(s):")],
    [sg.Text("",key = "globLocText")],
    [
        sg.Text("Instances of Public Data Members:"),
        sg.Text("",key = "PDMText"),
    ],
    [sg.Text("Location(s):")],
    [sg.Text("",key = "PDMLocText")],
    [
        sg.Text("Instances of Switch case use:"),
        sg.Text("",key = "switchText"),
    ],
    [sg.Text("Location(s):")],
    [sg.Text("",key = "switchLocText")],
    [
        sg.Text("Instances of Friend keyword use:"),
        sg.Text("",key = "friendText"),
    ],
    [sg.Text("Location(s):")],
    [sg.Text("",key = "friendLocText")],
    #=================================================================
    [sg.Text("Press Return if you wish to go back to the previous page")],
    [sg.Button("RETURN",key = "returnFromReportButton")],
]

layout = [
    [
    sg.Column(file_list_column,key = "fileColumn",visible=True),
    #sg.pin(sg.VSeperator()),
    sg.Column(header_viewer_column,key = "headerColumn",visible=True),
    sg.Column(source_viewer_column,key = "sourceColumn",visible=True),   
    sg.Column(report_viewer_column,key = "reportColumn",visible = False)],
]

window = sg.Window("Student code analyser", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "-FOLDER-":
        folder = values["-FOLDER-"] 
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
        try:
            headers,sources,countArr,occurArr = PrscC(os.path.join(folder))
            window["-TOUT-"].Update("Press VIEW to see the report on bad practice")
            window["impText"].Update(str(countArr[0]))
            window["impLocText"].Update(occurArr[0])
            window["globText"].Update(str(countArr[1]))
            window["globLocText"].Update(occurArr[1])
            window["PDMText"].Update(str(countArr[2]))
            window["PDMLocText"].Update(occurArr[2])
            window["switchText"].Update(str(countArr[3]))
            window["switchLocText"].Update(occurArr[3])
            window["friendText"].Update(str(countArr[4]))
            window["friendLocText"].Update(occurArr[4])
            
            #-------------------------------------------
            
            window["listHeaders"].Update(headers.keys())
            window["listSources"].Update(sources.keys())
            window["viewButton"].Update(visible = True)
        except:
            file_list = []
    if event == "viewButton":
        window["fileColumn"].Update(visible = False)
        window["headerColumn"].Update(visible = False)
        window["sourceColumn"].Update(visible = False)
        window["reportColumn"].Update(visible = True)
    if event == "-FILE LIST-":  # A file was chosen from the listbox
        print("butts")
    if event == "returnFromReportButton":
        window["fileColumn"].Update(visible = True)
        window["headerColumn"].Update(visible = True)
        window["sourceColumn"].Update(visible = True)
        window["reportColumn"].Update(visible = False)
    #if event =="listHeaders":
        
        
window.close()