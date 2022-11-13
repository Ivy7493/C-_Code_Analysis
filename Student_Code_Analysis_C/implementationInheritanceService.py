

def hasImplementationPresent(functionType,functionName,cppFile):
    functionStart = -1
    implementationFound = False
    bigScope = 0
    functionEnd =-1
    for line in cppFile: #Run through all lines
        implementationFound = False
        if (functionName in line) and (functionType in line) and ("(" in line and ")" in line ) and (line.find("(")>line.find(functionName)): #if we find the function okay cool
            functionStart = cppFile.index(line) #getting where it starts
            currentLine = functionStart
            scope = 0
            scopeProtect = True
            if('{' in line or '{' in cppFile[functionStart+1]):
                scope=1
                if " " in line:
                    if('{' in line and '}' in line and line.find(line.split(' ')[1]) == line.find(functionName) and "virtual" not in line and (line.find(functionName) < line.find('{')) and (line.find(functionName) < line.rfind('}'))):
                        scope=0
                        return str(functionStart)
                    
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
                    currentLine +=1
                
                functionEnd = currentLine
            if implementationFound:  
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
            elif '.h' in fileName and (scope <= 1 or ('{' not in file[file.index(line) + 1] and '{' not in line)):
                continue
            else:
                locations.append(fileName + '-' + str(file.index(line)))
    return locations



def extractImplementationTreeClassName(headers, source, className ,classNames,classLocations):
    if not className in classNames:
        return {}
    fileName = classLocations[classNames.index(className)].split("-")[0]
    file = headers[fileName]
    lineNumOfClass = int(classLocations[classNames.index(className)].split("-")[1])
    lineOfClass =file[lineNumOfClass]
    lineOfClass=lineOfClass.strip()
    nextLine=""
    try:
        nextLine = file[lineNumOfClass + 1]
        nextLine=nextLine.strip()
    except:
        pass
    if (':' in lineOfClass and "class" in lineOfClass and lineOfClass.find("class")==0) or (':' in nextLine and nextLine.find(":")==0):
        cleanline = ""
        workingLine = lineOfClass.strip()
        nextWorkingLine = nextLine.strip()
        if "::" in workingLine:
            workingLine=workingLine.replace("::","``")
        if "::" in nextWorkingLine:
            nextWorkingLine=nextWorkingLine.replace("::","``")
            
        if workingLine.find(':') == (len(workingLine) -1):
            try:
                cleanline = nextWorkingLine
            except:
                pass
        elif nextWorkingLine.find(':') == 0:
            cleanline = nextWorkingLine
            cleanline = cleanline.replace(":","")
        else:
            cleanline = workingLine.split(':')[1]
        cleanline = cleanline.rstrip('{')
        cleanline = cleanline.rstrip()
        cleanline = cleanline.lstrip()
     
        allInheritedClasses = []
        if("," in cleanline):
            workingCleanLine = cleanline.split(",")
            for x in workingCleanLine:
                temp = x.strip()
                temp = temp.rstrip()
                temp = temp.lstrip()
                temp = temp.split(" ")[1]
                if "``" in temp:
                    temp =temp.split("``")[1]
                allInheritedClasses.append(temp)
        else:
            if "``" in cleanline:
                cleanline =cleanline.split("``")[1]
            elif " " in cleanline:
                cleanline =cleanline.split(" ")[1]

            allInheritedClasses.append(cleanline)

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
            
    elif ':' not in lineOfClass and className in lineOfClass: #Here when we hit the bottom
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
            pass
        try:
            cpp=source[fileName.split(".")[0]+".cpp"]
        except:
            pass

        #Now that we got the  header  and cpp,  lets extract all functions from header
        if(header != []): #PS we only do this if we can actually find the header
            functionNames,functionTypes,functionPositions = extractAllFunctionsFromClass(classLines)
            implementedFunctions = []
            functionLocations = []
            functionFileType = []
            for function in functionNames:
                if(len(function) > 2):
                    if(cpp != []): # PS we can only look for implementation in cpp if there  is a cpp
                        cppImplementedCheck = hasImplementationPresent(functionTypes[functionNames.index(function)],function,cpp)
                        if(len(cppImplementedCheck) > 0):
                            implementedFunctions.append(function)
                            functionLocations.append(cppImplementedCheck)
                            functionFileType.append('.cpp')
                    headerImplementationCheck = hasImplementationPresent(functionTypes[functionNames.index(function)],function,header)
                    
                    if(len(headerImplementationCheck) > 0):
                        implementedFunctions.append(function)
                        functionLocations.append(headerImplementationCheck)
                        functionFileType.append('.h')
                        
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
    
    return ImplementedMembers
        

def findClassDeclaration(file,className):
    className = className.lower()
    for line in file:
        fixedLine = line.lower()
        if(className in fixedLine and 'class' in fixedLine and (fixedLine.find('class') < fixedLine.find(className)) and ' ' in fixedLine and fixedLine.find('class') == 0):
            return file.index(line)

def checkChainForImplementationInheritance(chain,source,headers):
    
    chain = chain[::-1] #reversing using list slicing
    counter = 1
    highlights = []
    linkCounter = 1
    for link in chain:
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
            functionCounter = 0
            for function in functions:
                resultCPP = []
                resultHeader = []
                if len(linkcpp)>0:
                    resultCPP = checkForUsage(function,linkcpp,link['classFile'] + '.cpp')
                if len(linkHeader) > 0 :
                    resultHeader = checkForUsage(function,linkHeader,link['classFile'] + '.h')
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
    output = extractImplementationTreeClassName(headers,source,className,classNames,classLocations); # class name, All classes, all class locations 1:1
    results = []
    output = convertToArrayOfInheritance(output)
    output.append(className)
    preChain = AnalyzeInheritanceChain(output,source,headers,classNames,classLocations,classScopes)
    results = checkChainForImplementationInheritance(preChain,source,headers)
    return list(set(results))

        