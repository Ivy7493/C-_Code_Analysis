

def hasImplementationPresent(functionType,functionName,cppFile):
    functionStart = -1
    implementationFound = False
    bigScope = 0
    functionEnd =-1
    #print("FILENAME FOR HAS IMPLEMENTATION PRESENT: ",functionName)
    for line in cppFile: #Run through all lines
        implementationFound = False
        if (functionName in line) and (functionType in line) and ("(" in line and ")" in line ) and (line.find("(")>line.find(functionName)): #if we find the function okay cool
            #print("We found Function: ", functionName)
            functionStart = cppFile.index(line) #getting where it starts
            currentLine = functionStart
            scope = 0
            scopeProtect = True
            #print('stage 1')
            if('{' in line or '{' in cppFile[functionStart+1]):
                #print('stage 2')
                scope=1
                if " " in line:
                    if('{' in line and '}' in line and line.find(line.split(' ')[1]) == line.find(functionName) and "virtual" not in line and (line.find(functionName) < line.find('{')) and (line.find(functionName) < line.rfind('}'))):
                        #print("stage 2.5")  
                        scope=0
                        return str(functionStart)
                    #print('stage 3')

                # print(" STARTING NUM:",functionStart)
                    
                while scope != 0:
                    if scopeProtect and "{" in cppFile[currentLine]: #used to ge through first line
                        scopeProtect = False
                    
                    elif '{' in cppFile[currentLine]:
                        scope += 1
                    if '}' in cppFile[currentLine]:
                        scope -= 1
                    #///Deals with determining if implementation has occured in file
                    if(len(cppFile[currentLine].strip()) > 1 and cppFile[currentLine].strip() != "}" and cppFile[currentLine].strip() != "{") and currentLine != cppFile.index(line):
                        implementationFound = True
                        #print("Implementation found for: ",functionName)
                    currentLine +=1
                
                functionEnd = currentLine
                # print("function END =",functionEnd)
            if implementationFound:
                # print("implementation Found ++++++++",str(functionStart) + '@' + str(functionEnd))    
                return str(functionStart) + '@' + str(functionEnd-1)
    return ""
                

def hasImplementationInHeader(headerFile,fileName):
    locationOccurrences = []
    for line in headerFile:
        if(("("  in line and ")" in line) and ("void" in line or "int" in line or "double" in line or "string" in line or "auto" in line or "char" in line or "bool" in line or "float" in line or "*" in line or "const" in line or "::" in line)):
            if('= 0' not in line or "=0" not in line): 
                nextline = headerFile[headerFile.index(line)+1]
                if(('{'in line or '}' in line)or ('{' in nextline and '(' not in nextline and ')' not in nextline)):
                    locationOccurrences.append(fileName +  "-" + str(headerFile.index(line)))
    return locationOccurrences


def extractAllFunctionsFromClass(headerFile):
    functionNames = []
    functionTypes = []
    functionPositions = []
    for line in headerFile:
        if(("("  in line and ")" in line) and " " in line and len(line.split(" ")) >= 2 and '~' not in line):
            functionNameEnd = line.find('(') - 1 # we need the functions name out of the header to search for in the cpp
            extractedName = ""
            for y in range(functionNameEnd,0, -1):
                if(line[y] != " "):
                    extractedName = line[y] + extractedName
                elif(line[y] == " "):
                    break

            #=====The following deals with extracting types from functions incase of overloading
            extractedType = ""
            extractedTypeEnd = line.find(" ")
            extractedType = line[0:extractedTypeEnd]
            if(extractedType == "virtual"):
                tempCurrentLine = ""
                counter =  extractedTypeEnd + 1
                while(line[counter] != " "):
                    tempCurrentLine = tempCurrentLine + line[counter]
                    counter+=1
                extractedType = tempCurrentLine
            if(extractedType != extractedName):
                functionNames.append(extractedName)
                functionTypes.append(extractedType)
                functionPositions.append(headerFile.index(line))

    return functionNames,functionTypes,functionPositions



def checkForUsage(functionName,file,fileName):
    locations = []
    scope = 0
    for line in file:
        if('{' in line):
            scope += 1
        if('}' in line):
            scope -= 1; 
        if(functionName in line and '(' in line and ')' in line and (line[line.find(functionName) + len(functionName)] == '(' or line[line.find(functionName) + len(functionName)] == ' (') and 'override' not in line and not ("=" in line and '0' in line and line.find('0') > line.find('=') )):
            if('::' in line and line.find('::') < line.find(functionName) and ' ' in line and line.find(" ") < line.find('::')):
                continue
            elif '.h' in fileName and scope <= 1:
                continue
            else:
                locations.append(fileName + '-' + str(file.index(line)))
        # if fileName == "PacMan.cpp":
        #     print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh", locations)
    return locations



def extractImplementationTreeClassName(headers, source, className ,classNames,classLocations):
    #print("For file: ", fileName)
    #print("$$$$$$$$$$$$$$$$$$$$$$")
    #print(line)
    if not className in classNames:
        return {}
    fileName = classLocations[classNames.index(className)].split("-")[0]
    file = headers[fileName]
    # print("$$$$$$$$$$$$$$$$$$$$$$ ",fileName," $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    lineNumOfClass = int(classLocations[classNames.index(className)].split("-")[1])
    lineOfClass =file[lineNumOfClass]
    lineOfClass=lineOfClass.strip()
    nextLine=""
    try:
        nextLine = file[lineNumOfClass + 1]
        nextLine=nextLine.strip()
    except:
        print("Next line out of index")
    # print("stage 1",lineOfClass)
    if (':' in lineOfClass and "class" in lineOfClass and lineOfClass.find("class")==0) or (':' in nextLine and nextLine.find(":")==0):
        # print("__:__ in line :", lineOfClass,"or : in the nextline:",nextLine)
        cleanline = ""
        workingLine = lineOfClass.strip()
        nextWorkingLine = nextLine.strip()
        if "::" in workingLine:
            # print(":: in working Line")
            workingLine=workingLine.replace("::","``")
            # print(workingLine)
        if "::" in nextWorkingLine:
            # print(":: in nextworking Line")
            nextWorkingLine=nextWorkingLine.replace("::","``")
            
        if workingLine.find(':') == (len(workingLine) -1):
            # print("Passed weird line")
            try:
                cleanline = nextWorkingLine
            except:
                print("Can't find it in the file for clean line i guess")
            # print("stage1")
        elif nextWorkingLine.find(':') == 0:
            cleanline = nextWorkingLine
            cleanline = cleanline.replace(":","")
        else:
            cleanline = workingLine.split(':')[1]
        cleanline = cleanline.rstrip('{')
        cleanline = cleanline.rstrip()
        cleanline = cleanline.lstrip()
        #print("stage 2")
     
        allInheritedClasses = []
        if("," in cleanline):
            workingCleanLine = cleanline.split(",")
            #print(workingCleanLine)
            for x in workingCleanLine:
                temp = x.strip()
                temp = temp.rstrip()
                temp = temp.lstrip()
                temp = temp.split(" ")[1]
                if "``" in temp:
                    # print("`` in cleanline in if statement")
                    temp =temp.split("``")[1]
                allInheritedClasses.append(temp)
        else:
            if "``" in cleanline:
                # print("`` in cleanline in else statement not if")
                cleanline =cleanline.split("``")[1]
            elif " " in cleanline:
                cleanline =cleanline.split(" ")[1]

            allInheritedClasses.append(cleanline)
            
        #print(" After fixing: ")
        #print(allInheritedClasses)

        tempWorkingObject = {
            "className" : className,
            "classesInheritedFrom" : allInheritedClasses,
            "inheritedObjects": [], 
            "classDeclaration": lineOfClass,
            "lineNumber" : lineNumOfClass,
            "fileName" : fileName
        }

        for inheritedClass in tempWorkingObject['classesInheritedFrom']:
            obj = extractImplementationTreeClassName(headers,source,inheritedClass,classNames,classLocations)
            tempWorkingObject['inheritedObjects'].append(obj)

        return tempWorkingObject
            
        returnedTree = []
        location = []
        for foundClass in allInheritedClasses:
            if foundClass in classNames:
                print("we found :", foundClass + '.h')
                nextInheritedHeaderFile = headers[classLocations[classNames.index(foundClass)].split('-')[0]]
                workingTree,workingLocation = extractImplementationTreeClassName(headers,source,foundClass,classNames,classLocations)
                # returnedTree,location = extractImplementationTree(nextInheritedHeaderFile,headers,source,NextInheritedClass + '.h')
                for branch in workingTree:
                    returnedTree.append(branch)
                for loc in workingLocation:
                    location.append(loc)
                returnedTree.append(foundClass)
                location.append(fileName + '-' + str((lineNumOfClass))); 
                continue           
        return returnedTree,location
    elif ':' not in lineOfClass and className in lineOfClass: #Here when we hit the bottom
        # print("ELSE TRIGGERED IN TREE IN IMPLEMENTATION")
        tempWorkingObject = {
            "className" : className,
            "classesInheritedFrom" : [],
            "inheritedObjects": [], 
            "classDeclaration": lineOfClass,
            "lineNumber" : lineNumOfClass,
            "fileName" : fileName
        }
        return tempWorkingObject
    else:
        return {}

def AnalyzeInheritanceChain(chain,source,headers,classNames,classLocations,classScopes):
    ImplementedMembers = []
    for member in chain:
        #print("We working with: ", member)
        fileName = classLocations[classNames.index(member)].split("-")[0]
        fileScope = classScopes[classNames.index(member)]
        fileScopeStart=int(fileScope.split("@")[0])
        fileScopeEnd=int(fileScope.split("@")[1])
        file = headers[fileName]
        classLines = file[fileScopeStart:fileScopeEnd]
        lineNumOfClass = int(classLocations[classNames.index(member)].split("-")[1])
        lineOfClass =file[lineNumOfClass]
        nextLine  =""
        header = []
        cpp = []

        #We gonna try get the header and cpp file
        try:
            header = headers[fileName.split(".")[0]+".h"]
        except:
            print("oops couldnt find header",fileName.split(".")[0])
        try:
            cpp=source[fileName.split(".")[0]+".cpp"]
        except:
            print("oops couldnt find source",fileName.split(".")[0])

        #Now that we got the  header  and cpp,  lets extract all functions from header
        if(header != []): #PS we only do this if we can actually find the header
            functionNames,functionTypes,functionPositions = extractAllFunctionsFromClass(classLines)
            #now we are gonna loop through all function names and only keep those with implementation
            #print("Extracted functions:")
            #print(functionNames)
            implementedFunctions = []
            functionLocations = []
            functionFileType = []
            for function in functionNames:
                if(len(function) > 2):
                    if(cpp != []): # PS we can only look for implementation in cpp if there  is a cpp
                        #print("Function Name: ", function)
                        cppImplementedCheck = hasImplementationPresent(functionTypes[functionNames.index(function)],function,cpp)
                        #print("Declaration range: ", cppImplementedCheck)
                        if(len(cppImplementedCheck) > 0):
                            implementedFunctions.append(function)
                            functionLocations.append(cppImplementedCheck)
                            functionFileType.append('.cpp')
                    headerImplementationCheck = hasImplementationPresent(functionTypes[functionNames.index(function)],function,header)
                    
                    if(len(headerImplementationCheck) > 0):
                        implementedFunctions.append(function)
                        functionLocations.append(headerImplementationCheck)
                        functionFileType.append('.h')
            #print("implemented functions:")
            #print(implementedFunctions)
            #Now we gonna combine the results for the inheritance object
            if(len(implementedFunctions) > 0): #PS we only wanna append something if there is something to append
                entry = {
                    'class' : member,
                    'implementedFunctions' : implementedFunctions,
                    'functionLocations' : functionLocations,
                    'fileTypes' : functionFileType,
                    'classFile' : classLocations[classNames.index(member)].split("-")[0].split(".")[0],
                    'classLine' : lineNumOfClass
                }
                ImplementedMembers.append(entry)
    #print("Inheritance Chain")
    #print(ImplementedMembers)
    
    return ImplementedMembers
        

def findClassDeclaration(file,className):
    #print("looking in: ",  className)
    #print(file)
    className = className.lower()
    for line in file:
        fixedLine = line.lower()
        if(className in fixedLine and 'class' in fixedLine and (fixedLine.find('class') < fixedLine.find(className)) and ' ' in fixedLine and fixedLine.find('class') == 0):
            #print("YEEE FOUND IT", className)
            return file.index(line)

def checkChainForImplementationInheritance(chain,source,headers):
    
    chain = chain[::-1] #reversing using list slicing
    counter = 1
    highlights = []
    linkCounter = 1
    for link in chain:
        #print("For: ", link['class'])
        workingChain = chain
        linkHeader = []
        linkcpp = []
        if link['classFile'] + '.h' in headers:
            linkHeader = headers[link['classFile'] + '.h']
        if link['classFile'] + '.cpp' in source:
            linkcpp = source[link['classFile'] + '.cpp']
        for i in range(counter):
            workingChain.pop(0)
        for workingLink in workingChain:
            functions = workingLink['implementedFunctions']
            functionLocations = workingLink['functionLocations']

            #print(link['class'] + ' has the function scope of : ')
            #print(functions)
            #print("Stage 3")
            functionCounter = 0
            for function in functions:
                #print("For Function: ", function)
                resultCPP = []
                resultHeader = []
                if len(linkcpp)>0:
                    resultCPP = checkForUsage(function,linkcpp,link['classFile'] + '.cpp')
                if len(linkHeader) > 0 :
                    resultHeader = checkForUsage(function,linkHeader,link['classFile'] + '.h')
                #print("Did we find Implementation?: ")
                #print(resultHeader)
                #print(resultCPP)
                for x in resultHeader:
                    highlights.append(x)
                    highlights.append(workingLink['classFile'] + workingLink['fileTypes'][functionCounter] +'-' + functionLocations[functionCounter])
                    highlights.append(link['classFile'] + '.h' + '-' + str(link['classLine']))
                
                for x in resultCPP:
                    highlights.append(x)
                    highlights.append(workingLink['classFile'] + workingLink['fileTypes'][functionCounter] + '-' + functionLocations[functionCounter])
                    highlights.append(workingLink['classFile'] + '.h' + '-' + str(workingLink['classLine']))
                    highlights.append(link['classFile'] + '.h' + '-' + str(link['classLine']))
                functionCounter += 1  
        counter += 1
        linkCounter+=1

    return highlights
       
def convertToArrayOfInheritance(inheritanceChain):
    outputChain = []
    currentNode = inheritanceChain['inheritedObjects']
    for x in currentNode:
        if(x):
            outputChain.append(x['className'])
            resultChain = convertToArrayOfInheritance(x)
            for y in resultChain:
                outputChain.append(y)
            

    return outputChain
            
    
            
            
        


def analyzeImplementationInheritance(source,headers,className,classNames,classLocations,classScopes):
    #  originalFile = classLocation.split('-')[0]
    print("====================== " + className + " ======================")
    output = extractImplementationTreeClassName(headers,source,className,classNames,classLocations); # class name, All classes, all class locations 1-1
    # output.append(className)
    # print("TREEE IN IMPLEMENTATION->",output)
    #print(output)

    
    results = []
    output = convertToArrayOfInheritance(output)
    #print("ANALYZE IMPLEMENTATION INHERITANCE: ",output)
    print (" OUTPUT OF COVERSION:")
    output.append(className)
    print(output)
    preChain = AnalyzeInheritanceChain(output,source,headers,classNames,classLocations,classScopes)
    results = checkChainForImplementationInheritance(preChain,source,headers)
    #print("This Chains Inheritance issues results:")
    #print(results)
    #print("This Chains Inheritance issues output:",output)
    #print('========================================================')
    print(results)
    return list(set(results))

        