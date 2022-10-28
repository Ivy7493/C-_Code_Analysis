
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


        #=================Running Tree of program======#

    totalDependencies = []
    for headerName in headers:
        # print(headerName)
        try:
            tree,location = extractTypeTree(headers[headerName],headers,headerName)
            # print(tree)
            tree.append(headerName.split(".")[0])
            totalDependencies.append(tree)
        except:
            print("noneTYpe")

    # print("OOOGA BOOOGA: ")
    # print(totalDependencies)
    # print("=================")
    dependencyDiagram=[]
    baseClasses =[]
    firstInstance=True
    dependencyDictionary = {}
    baseClasses = []
    for dependency in totalDependencies:
        if(len(dependency) == 1):
            baseClasses.append(dependency[0])
        for entity in dependency:
                if dependency.index(entity) + 1 < len(dependency):
                    # print("STAGE 1")
                    if not entity in dependencyDictionary:
                        # print("STAGE 2")
                        dependencyDictionary[entity] = []
                        # print("STAGE 2.5")
                        dependencyDictionary[entity].append(dependency[dependency.index(entity) + 1])
                        # print("STAGE 3")
                    else:
                        # print("STAGE 4")
                        dependencyDictionary[entity].append(dependency[dependency.index(entity) + 1])
    #                     print("STAGE 5")
    # print("HOOOOOOOOOOOOOOOOOOOOOOOOOHAAA")
    for file in dependencyDictionary:
        dependencyDictionary[file] = list(set(dependencyDictionary[file]))
        print("Class: ", file)
        print("CLASS DEPENDENCY DICTIONARY FILE: ",dependencyDictionary[file])
        
    print("And now for the classes that don't inherit fromo another class: ")
    print(baseClasses)
    treeConstruction = generateUML(baseClasses,dependencyDictionary,0)

    # ===============================This creates the html reponsible for generating the uml=============
    
    fullFile =""
    print("YOLO")
    print(treeConstruction)
    
    scopeCount=0
    lastScope=''
    xFile=''
    for x in treeConstruction: 
        # print("I want to know what lastscope is always: ",lastScope)
        xFile= x +'.h'
        if '{' in x:
            scopeCount+=1
            #print( "HERE =======",scopeCount)
            if scopeCount==1:
                # fullFile+= '\n'+"<div>"
                lastScope="sep"
            else:
                #print("larger than 1 scope count and in {")
                fullFile += '\n' + '<ul>'+'\n'
                if lastScope=="sep":
                    #print("THIS IS WHERE LAST SCOPE IS CHNGED TO TOGETHER: ",scopeCount)
                    lastScope="together"
                else:
                    #print("this is where lastscope set to nothing ")
                    lastScope=""
        if '}' in x:
            scopeCount-=1
            if scopeCount==1:
                #print(" if in in }")
                fullFile+= '</ul>'+'\n'+"</div>"
            else:
                #print("else in }")
                fullFile += '\n' + '</li>'+'</ul>'
        
        if '{' not in x and '}' not in x and (lastScope!="sep" and lastScope!="together"and scopeCount!=1):
            #print("Generic statement",x)
            fullFile+= "<li>"+"<form method='post'>"+'\n'+'{% csrf_token %}'+"<input type='hidden' name='issue' value='implementation' />"+"<button id='buttonList' type='submit' value="+"'"+xFile +"'"+"name='key' formaction='displayCode/'>" + x +"</button>"+"</form>"+"</li>"+"\n"
            
        elif'{' not in x and '}' not in x and (lastScope=="sep" and scopeCount==1):
            #print("this only occurs if lastscope=sep and scopecount =1")
            fullFile+= "<div class='tree col-sm-auto'>"+"\n" + "<li>"+"<form method='post'>"+'\n'+'{% csrf_token %}'+"<input type='hidden' name='issue' value='implementation' />"+"<button id='buttonList' type='submit' value="+"'"+xFile +"'"+" name='key' formaction='displayCode/'>" + x +"</button>"+"</form>"+"</li>"+'\n'+'</div>'
            
        elif'{' not in x and '}' not in x and (lastScope=="together" and scopeCount==2):
            #print ("This is where last div is removed from line:", lastScope)
            fullFile=removeLastOccurrence(fullFile,"</div>",len(fullFile),6)
            fullFile+= "<li>"+"<form method='post'>"+'\n'+'{% csrf_token %}'+"<input type='hidden' name='issue' value='implementation' />"+"<button id='buttonList' type='submit' value="+"'"+xFile +"'"+" name='key' formaction='displayCode/'>" + x +"</button>"+"</form>"+"</li>"
            lastScope=""
        
        elif '{' not in x and '}' not in x and (lastScope!="sep" and lastScope!="together"and scopeCount==1):
            #print("Generic statement MARK @",x)
            fullFile+= "<div class='tree col-sm-auto'>"+"<li>"+"<form method='post'>"+'\n'+'{% csrf_token %}'+"\n"+"<input type='hidden' name='issue' value='implementation' />"+"<button id='buttonList' type='submit' value="+"'"+xFile +"'"+" name='key' formaction='displayCode/'>" + x +"</button>"+"</form>"+"</li>"+"\n"+"</div>"+"\n"
        #print("+",fullFile)
    #print("+",fullFile)

    try:
        os.remove(os.path.join('fileSelect','templates','fileSelect','tree.html'))
    except:
        print("Not tree html found")
    
    with open(os.path.join('fileSelect','templates','fileSelect','tree.html'), "w+") as file:
        file.write(fullFile)


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


def generateUML(baseClasses,UMLstruct,count):
    if(count == 0):
        print('}')
        temp = getData('tree')
        temp.append('}')
        saveData('tree', temp)
    #print('->',baseClass)
    for baseClass in baseClasses:
        if(baseClass in UMLstruct):
            if(len(UMLstruct[baseClass]) > 0):
                # print("we in here")
                print('}')
                temp = getData('tree')
                temp.append('}')
                saveData('tree', temp)
                for x in UMLstruct[baseClass]:
                    generateUML([x],UMLstruct,count + 1)
                    print(x)
                    temp = getData('tree')
                    temp.append(x)
                    saveData('tree',temp)
                print('{') #old start
                temp = getData('tree')
                temp.append('{')
                saveData('tree', temp)
        if(count == 0):
            print(baseClass)
            temp = getData('tree')
            temp.append(baseClass)
            saveData('tree', temp)
    if(count == 0):
        print('{')
        temp = getData('tree')
        temp.append('{')
        saveData('tree', temp[::-1])
        #print(getData('tree'))
        return getData('tree')


def displayCode(request):
    # saveData('tree',[])   
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
                        counter += 1
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