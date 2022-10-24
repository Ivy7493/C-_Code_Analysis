
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.test import TestCase
from numpy import append
from listings.pathForm import getPath
from ProcessController import ProcessController as PrscC
import os
from persistentService import saveData,getData
from tkinter import filedialog
from tkinter import *
import concurrent.futures

def fileSelectHome(request):
    saveData('folder',"")
    form = getPath()
    return render(request,'fileSelect/fileSelectHome.html',{'form':form})


def select_folder():
    root = Tk()
    root.withdraw()
    
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    ttl = 'Select File'
    root.attributes("-topmost",1)
    
    root.folder_path = filedialog.askdirectory(parent=root,title=ttl)
    root.destroy()
    return root.folder_path


def navBarLaunch(request):
    saveData("folder","")
    return executeProgram(request)


def executeProgram(request):
    buttonVal = ""
    try:
        buttonVal = request.POST["folderName"]
    except:
        print("do not need to restart");

    folder = ""
    if(buttonVal != "restart"):
        folder = getData("folder")
    if(folder == ""):
        # print("this hit ======================")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(select_folder)
            folder = future.result()
            saveData('folder',folder)
        # print(folder)

    headers,sources,occurArr = PrscC(os.path.join(folder))
    saveData('issues',occurArr)
    saveData('headers',headers)
    saveData('sources',sources)

    occurArrFile = []
    for x in occurArr:
        newList = []
        for y in x:
            if('@' in y):
                firstStage = y.split('@')
                for item  in firstStage:
                    temp = y.split('-')
                    newList.append(temp[0])
            else:
                temp = y.split('-')
                newList.append(temp[0])
        occurArrFile.append(list(set(newList)))

    context = {
        'title':'File Viewer',
        'headers':headers,
        'sources':sources,
        'implementationIssues':occurArrFile[0],
        'globalVarIssues':occurArrFile[1],
        'publicDataIssues':occurArrFile[2],
        'switchIssues':occurArrFile[3],
        'friendIssues':occurArrFile[4],
        'dryIssues' : occurArrFile[5]
    }
    
    return render(request,'fileSelect/fileDisplay.html',context)

def viewReport(request):
    return render(request,'fileSelect/fileDisplay.html',{'title':'File Viewer'})

def displayCode(request):
    try:
        fileName = request.POST["key"]
    except:
        print('no filename provided')
        
    issueId = ""
    try:
        issueId = request.POST["issue"]
    except:
        issueId = "allIssues"
        print("Caught Empty issueID")
        
    file =[]
    if ".h" in fileName:
        file = getData('headers')[fileName]
    elif ".cpp" in fileName:
        file = getData("sources")[fileName]
    issues = getData("issues")
    allIssuesArray = []
    linesOfIssues = []
    lineColours = []
    for typeOfProblem in issues:
        colorClass = ""
        if(issues.index(typeOfProblem) == 0): #Implementation
            colorClass = "bg-primary"
        elif(issues.index(typeOfProblem) == 1): #Global
            colorClass = "bg-secondary"
        elif(issues.index(typeOfProblem) == 2): #Public
            colorClass = "table-danger"
        elif(issues.index(typeOfProblem) == 3): #Switch
            colorClass = "bg-danger"
        elif(issues.index(typeOfProblem) == 4): #Friend
            colorClass = "bg-warning"
        elif(issues.index(typeOfProblem) == 5): #DRY
            colorClass = 'table-success'
        for fileIssues in typeOfProblem:
            tempSplit = fileIssues.split('-')
            if(tempSplit[0] == fileName):
                #print("Start::::::::::")
                #print("Range Extracted: ", tempSplit[1])
                if('@' in tempSplit[1]):
                    #print("Range Deticated!")
                    data = tempSplit[1].split('@')
                    #print("Range SPlit: ")
                    #print(data[0])
                    #print(data[1])
                    counter = int(data[0])
                    end = int(data[1])
                    while(counter != end):
                        linesOfIssues.append(counter)
                        lineColours.append(colorClass)
                        counter += 1;
                else:
                    linesOfIssues.append(int(tempSplit[1]))
                    lineColours.append(colorClass)
        allIssuesArray.append(linesOfIssues) 
        linesOfIssues = []
    #print("Issue lines for file:" )
    lineStatus = [False] * len(file)
    convertedColour = [""]*len(file)
    totalString = ""
    key = 0
    if(issueId == "implementation"):
        key = 0
    elif(issueId == "global"):
        key = 1
    elif(issueId == "publicData"):
        key = 2
    elif(issueId == "switch"):
        key = 3
    elif(issueId == "friend"):
        key = 4
    elif(issueId == "dry"):
        key = 5
    elif(issueId == "allIssues"):
        tempArray = []
        for x in allIssuesArray:
            for y in x:
                tempArray.append(y)
        allIssuesArray.append(tempArray)
        key = 6
       
    for x in allIssuesArray[key]:
        lineStatus[x] = True
        convertedColour[x] = lineColours.pop(0)
    locationArray  = ""

    counter = 0;
    for x in lineStatus:
        if(x):
            locationArray = locationArray + ',' + str((counter + 1))
        counter += 1;
    for x in file:
        totalString += x;
    context = {
        'file':file,
        'lineStatus':lineStatus,
        'lineColour': convertedColour,
        'fileName': fileName,
        'totalString': totalString,
        'highlight': locationArray,
        'issue': issueId
    }
    return render(request,'fileSelect/displayCode.html',context)