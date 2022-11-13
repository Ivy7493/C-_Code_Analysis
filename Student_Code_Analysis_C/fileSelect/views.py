
from django.shortcuts import render
from numpy import append
from listings.pathForm import getPath
from ProcessController import ProcessController as PrscC
from implementationInheritanceService import extractImplementationTreeClassName
import os
from persistentService import saveData,getData
from tkinter import *
from tkinter import filedialog
import concurrent.futures

def information(request):
    return render(request,'fileSelect/information.html')

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




# This runs when the program needs to display the main issue page /fileDisplay.html
def removeLastOccurrence(initialString, stringToRemove, inputSize, stringToRemoveSize):
    initialString = [i for i in initialString]
    stringToRemove = [i for i in stringToRemove]
 
    # If stringToRemoveSize is greater than inputSize
    if (stringToRemoveSize > inputSize):
        return initialString
 
    # Iterate while i is greater than
    # or equal to 0
    for i in range(inputSize - stringToRemoveSize, -1, -1):
        # of stringToRemove has
        # been found or not
        flag = 0
 
        # Iterate over the range [0, stringToRemoveSize]
        for j in range(stringToRemoveSize):
            # If S[j+1] is not equal to
            # stringToRemove[j]
            if (initialString[j + i] != stringToRemove[j]):
 
                # Mark flag true and break
                flag = 1
                break
 
        # If occurrence has been found
        if (flag == 0):
 
            # Delete the subover the
            # range [i, i+stringToRemoveSize]
            for j in range(i,inputSize-stringToRemoveSize):
                initialString[j] = initialString[j + stringToRemoveSize]
 
            # Resize the initialstring
            initialString = initialString[:inputSize - stringToRemoveSize]
            break
 
    # Return new string
    return "".join(initialString)

def executeProgram(request):
    saveData('tree',[])
    buttonVal = ""
    try:
        buttonVal = request.POST["folderName"]
    except:
        pass

    folder = ""
    if(buttonVal != "restart"):
        folder = getData("folder")
    if(folder == ""):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(select_folder)
            folder = future.result()
            saveData('folder',folder)

    headers,sources,occurArr = PrscC(os.path.join(folder))
    saveData('issues',occurArr)
    saveData('headers',headers)
    saveData('sources',sources)
    classNames=getData("classNames")
    classLocations=getData("classNameLocations")
    processedHeaders=getData("processedHeaders")
    processedSources=getData("processedSources")

    occurArrFile_H = []
    occurArrFile_C=[]
    for x in occurArr:
        newList_H = []
        newList_C=[]
        for y in x:
            if('@' in y):
                firstStage = y.split('@')
                for item  in firstStage:
                    temp = y.split('-')
                    if ".h" in temp[0]:
                        newList_H.append(temp[0])
                    else:
                        newList_C.append(temp[0])
            else:
                temp = y.split('-')
                if ".h" in temp[0]:
                    newList_H.append(temp[0])
                else:
                    newList_C.append(temp[0])
        occurArrFile_H.append(list(set(newList_H)))
        occurArrFile_C.append(list(set(newList_C)))


#=================Running Tree of program======#

    totalDependencies = []
    tree = []
    for className in classNames:
        try:
            tree = extractImplementationTreeClassName(processedHeaders, processedSources, className ,classNames,classLocations)
            totalDependencies.append(tree)
        except:
            pass


    dependencyDiagram=[]
    baseClasses =[]
    firstInstance=True
    dependencyDictionary = {}
    baseClasses = []
    for dependency in totalDependencies:

        for entity in dependency['classesInheritedFrom']:
            if entity not in dependencyDictionary:
                dependencyDictionary[entity] = []
                dependencyDictionary[entity].append(dependency['className'])
            else:
                dependencyDictionary[entity].append(dependency['className'])

    for file in dependencyDictionary:
        dependencyDictionary[file] = list(set(dependencyDictionary[file]))

    scopeCount=0
    lastScope=''
    fullFile='<pre class="mermaid"><code>'+'\n'"classDiagram"+'\n'
    if dependencyDictionary:
        for key in dependencyDictionary:
            if dependencyDictionary[key]:
                if len(dependencyDictionary[key])>0:
                    for classFile in dependencyDictionary[key]:
                        fullFile+=key+"&lt;--"+classFile+'\n'
                else:
                    fullFile+=key+'\n'
        fullFile+="</code></pre>"
    
    else:
        fullFile='<h3> No inheritance detected in this program </h3>'

    
    
    try:
        os.remove(os.path.join('fileSelect','templates','fileSelect','tree.html'))
    except:
        pass
    
    with open(os.path.join('fileSelect','templates','fileSelect','tree.html'), "w+") as file:
        file.write(fullFile)


    context = {
        'title':'File Viewer',
        'headers':headers,
        'sources':sources,
        'implementationIssues_H':occurArrFile_H[0],
        'implementationIssues_C':occurArrFile_C[0],
        'implementationLength':len(occurArrFile_C[0])+len(occurArrFile_H[0]),
        'globalVarIssues_H':occurArrFile_H[1],
        'globalVarIssues_C':occurArrFile_C[1],
        'globalLength':len(occurArrFile_C[1])+len(occurArrFile_H[1]),
        'publicDataIssues_H':occurArrFile_H[2],
        'publicDataIssues_C':occurArrFile_C[2],
        'publicLength':len(occurArrFile_C[2])+len(occurArrFile_H[2]),
        'switchIssues_H':occurArrFile_H[3],
        'switchIssues_C':occurArrFile_C[3],
        'switchLength':len(occurArrFile_C[3])+len(occurArrFile_H[3]),
        'friendIssues_H':occurArrFile_H[4],
        'friendIssues_C':occurArrFile_C[4],
        'friendLength':len(occurArrFile_C[4])+len(occurArrFile_H[4]),
        'dryIssues_H' : occurArrFile_H[5],
        'dryIssues_C' : occurArrFile_C[5],
        'dryLength':len(occurArrFile_C[5])+len(occurArrFile_H[5]),
        'mermaidText':fullFile,
    }

    
    return render(request,'fileSelect/fileDisplay.html',context)


def generateUML(baseClasses,UMLstruct,count):
    if(count == 0):
        temp = getData('tree')
        temp.append('}')
        saveData('tree', temp)
    for baseClass in baseClasses:
        if(baseClass in UMLstruct):
            if(len(UMLstruct[baseClass]) > 0):
                temp = getData('tree')
                temp.append('}')
                saveData('tree', temp)
                for x in UMLstruct[baseClass]:
                    generateUML([x],UMLstruct,count + 1)
                    temp = getData('tree')
                    temp.append(x)
                    saveData('tree',temp)
                temp = getData('tree')
                temp.append('{')
                saveData('tree', temp)
        if(count == 0):
            temp = getData('tree')
            temp.append(baseClass)
            saveData('tree', temp)
    if(count == 0):
        temp = getData('tree')
        temp.append('{')
        saveData('tree', temp[::-1])
        return getData('tree')


def displayCode(request):
    fileName=""
    try:
        fileName = request.POST["key"]
    except:
        pass
        
    issueId = ""
    try:
        issueId = request.POST["issue"]
    except:
        issueId = "allIssues"
        
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
                        counter += 1
                else:
                    linesOfIssues.append(int(tempSplit[1]))
        allIssuesArray.append(linesOfIssues) 
        linesOfIssues = []
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

    counter = 0
    for x in lineStatus:
        if(x):
            locationArray = locationArray + ',' + str((counter + 1))
        counter += 1
    for x in file:
        totalString += x     

    treeInfo=getData('tree')

    context = {
        'fileName': fileName,
        'totalString': totalString,
        'highlight': locationArray,
        'issue': issueId,
        'treeInfo':treeInfo,
    }
    return render(request,'fileSelect/displayCode.html',context)