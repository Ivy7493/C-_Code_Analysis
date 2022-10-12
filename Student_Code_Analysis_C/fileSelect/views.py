from fileinput import filename
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from listings.pathForm import getPath
from django.urls import reverse
from ProcessController import ProcessController as PrscC
import os
from ast import literal_eval
from persistentService import saveData,getData

def fileSelectHome(request):
    
    form = getPath()
   
    return render(request,'fileSelect/fileSelectHome.html',{'form':form})


def executeProgram(request):
    folder = request.POST["filePath"]
    headers,sources,occurArr = PrscC(os.path.join(folder))
    saveData('issues',occurArr)
    saveData('headers',headers)
    saveData('sources',sources)
    
    context = {
        'title':'File Viewer',
        'headers':headers,
        'sources':sources,
        'implementationIssues':occurArr[0],
        'globalVarIssues':occurArr[1],
        'publicDataIssues':occurArr[2],
        'switchIssues':occurArr[3],
        'friendIssues':occurArr[4],
        'dryIssues' : occurArr[5]
    }
    
    
    return render(request,'fileSelect/fileDisplay.html',context)

def viewReport(request):
    return render(request,'fileSelect/fileDisplay.html',{'title':'File Viewer'})

def displayCode(request):
    print("Hello?")
    fileName = request.POST["key"]
    print(fileName)
    file =[];
    if ".h" in fileName:
        file = getData('headers')[fileName]
    elif ".cpp" in fileName:
        file = getData("sources")[fileName]
    issues = getData("issues")
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
    print("Issue lines for file:" )
    lineStatus = [False] * len(file)
    convertedColour = [""]*len(file)
    for x in linesOfIssues:
        lineStatus[x] = True
        convertedColour[x] = lineColours.pop(0)
    
    context = {
        'file':file,
        'lineStatus':lineStatus,
        'lineColour': convertedColour,
        'fileName': fileName
    }
    print(linesOfIssues)
    return render(request,'fileSelect/displayCode.html',context)