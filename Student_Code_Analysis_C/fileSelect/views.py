
from django.shortcuts import render
from numpy import append
from listings.pathForm import getPath
from ProcessController import ProcessController as PrscC
from switchService import extractTypeTree
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
    for typeOfProblem in issues:
        for fileIssues in typeOfProblem:
            tempSplit = fileIssues.split('-')
            if(tempSplit[0] == fileName):
                if('@' in tempSplit[1]):
                    data = tempSplit[1].split('@')
                    counter = int(data[0])
                    end = int(data[1])
                    while(counter != end):
                        linesOfIssues.append(counter)
                        counter += 1;
                else:
                    linesOfIssues.append(int(tempSplit[1]))
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
    locationArray  = ""

    counter = 0;
    for x in lineStatus:
        if(x):
            locationArray = locationArray + ',' + str((counter + 1))
        counter += 1;
    for x in file:
        totalString += x;
    tree = []
    try:
        headers = getData("headers")
        tempName = fileName.split('.')[0]
        for x in headers:
            if(tempName +'.h' == x):
                print("YUUP we found a match")
                print(x)
        currentFileHeader = headers[tempName + '.h']
        totalDependencies = []
        for headerName in headers:
            print(headerName)
            try:
                tree,location = extractTypeTree(headers[headerName],headers,headerName)
                print(tree)
                tree.append(headerName.split(".")[0])
                totalDependencies.append(tree)
            except:
                print("noneTYpe")

        print("OOOGA BOOOGA: ")
        print(totalDependencies)
        print("=================")
        dependencyDiagram=[]
        baseClasses =[]
        firstInstance=True
        dependencyDictionary = {}
        for dependency in totalDependencies:
            for entity in dependency:
                   if dependency.index(entity) + 1 < len(dependency):
                        print("STAGE 1")
                        if not entity in dependencyDictionary:
                            print("STAGE 2")
                            dependencyDictionary[entity] = []
                            print("STAGE 2.5")
                            dependencyDictionary[entity].append(dependency[dependency.index(entity) + 1])
                            print("STAGE 3")
                        else:
                            print("STAGE 4")
                            dependencyDictionary[entity].append(dependency[dependency.index(entity) + 1])
                            print("STAGE 5")
            
        #     if len(dependency)==2 and firstInstance:
        #         dependencyDiagram.append(dependency)
        #         baseClasses.append(dependency[0])
        #         firstInstance=False;
        #         print("lendependency = 2")
        #     elif len(baseClasses)>0:
        #         print("BUTTTTTTTTTTTTTTTTTTTTTT")
        #         for nextDependency in totalDependencies:
        #             print(dependencyDiagram.index(dependency))
        #             if dependencyDiagram[dependencyDiagram.index(dependency)]!=nextDependency:
        #                 print("not the same")
        #                 if dependencyDiagram[totalDependencies.index(dependency)][0]==nextDependency[0]:
        #                     dependencyDiagram[totalDependencies.index(dependency)].append(dependency[1])
        # print ("DEPENDENCYDIAGRAM")
        # print(dependencyDiagram)
        print("HOOOOOOOOOOOOOOOOOOOOOOOOOHAAA")
        for file in dependencyDictionary:
            print("Class: ", file)
            print(dependencyDictionary[file])    
                
        # tree.append(fileName.split(".")[0])
        # print("For file: ", fileName.split(".")[0])
        # print(tree)
        # tree = tree[::-1]

    except:
        print("Pooping out")
    
    # if(len(tree) == 1):
    #     tree = []


    for branch in tree:
        currentNode = tree.index(branch)
        for next in tree:
            if tree.index(next) != currentNode:
                if tree[currentNode]==next:
                    tree[currentNode]=tree[currentNode] +".h"
                    next = next+".cpp"

    thereIsTree =False
    if len(tree) > 0:
        thereIsTree = True
            
    context = {
        'fileName': fileName,
        'totalString': totalString,
        'highlight': locationArray,
        'totalDependencies': totalDependencies,
        'issue': issueId,
        'thereIsTree':thereIsTree,
    }
    return render(request,'fileSelect/displayCode.html',context)