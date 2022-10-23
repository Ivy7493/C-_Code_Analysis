
def hasImplementationPresent(functionType,functionName,cppFile):
    functionStart = -1
    implementationFound = False
    for line in cppFile: #Run through all lines
        implementationFound = False
        if((functionName in line) and (functionType in line) and ("(" in line and ")" in line )): #if we find the function okay cool
            functionStart = cppFile.index(line) #getting where it starts
            currentLine = functionStart
            scope = 0
            scopeProtect = True
            if('{' in line or '{' in cppFile[functionStart+1]):
                while('}' not in cppFile[currentLine] and (scope != 0 or scopeProtect)):
                    if(scopeProtect and "{" in cppFile[currentLine]): #used to ge through first line
                        scopeProtect = False
                    #///Deals with determining if implementation has occured in file
                    if(len(cppFile[currentLine].strip()) > 1 and cppFile[currentLine].strip() != "}" and cppFile[currentLine].strip() != "{") and currentLine != cppFile.index(line):
                        implementationFound = True

                    if('{' in cppFile[currentLine]):
                        scope += 1
                    if('}' in cppFile[currentLine]):
                        scope -= 1
                    currentLine +=1
                functionEnd = currentLine
            if(implementationFound):
                return str(functionStart) + '@' + str(functionEnd)
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
    #print("Name of Header: ", headerFile)
    functionNames = []
    functionTypes = []
    functionPositions = []
    for line in headerFile:
        if(("("  in line and ")" in line) and ("void" in line or "int" in line or "double" in line or "string" in line or "auto" in line or "char" in line or "bool" in line or "float" in line or "*" in line or "const" in line)):
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
    for line in file:
        if(functionName in line and '(' in line and ')' in line):
            locations.append(fileName + '-' + str(file.index(line)))
    return locations


def analyzeImplementationInheritance(file,source,headers,passedFileName):
    newLocationOccurrences = []
    currentLine = 0
    extractClassName = ''

    #OG FILE FOR CHECUSAGE
    originalFile = passedFileName.split('.')[0]
    originalHeader = file
    canSearchOGFile = False
    try:
        originalCPP = source[originalFile + '.cpp']
        canSearchOGFile = True
    except:
        print("woah cant find the og cpp")

    for line in file:

        #This checks to see whether a class inherits from a base class and then finds the base class

        if(("private"in line or "protected" in line or "public" in line) and "class" in line and ':' in line):
            cleanline = line.rstrip()
            lastSpacePos = cleanline.rfind(' ')
            extractClassName = cleanline[lastSpacePos+1:]
            canFindCpp = True
            baseClassHeaderFile = []
            baseClassSourceFile = []

            try:
                baseClassHeaderFile = headers[extractClassName+'.h']
            except:
                continue
            try:
                 baseClassSourceFile = source[extractClassName + '.cpp']
            except:
                canFindCpp = False

            headerLocations = hasImplementationInHeader(baseClassHeaderFile,extractClassName + '.h')
            headerFunctionNames,headerFunctionTypes,headerFunctionPositions = extractAllFunctionsFromClass(baseClassHeaderFile)
           
            for i in range(len(headerFunctionNames)):
                test = hasImplementationPresent(headerFunctionTypes[i],headerFunctionNames[i],baseClassHeaderFile)

                if(len(test) > 0):
                    if(canSearchOGFile):
                        aretheyUsed = checkForUsage(headerFunctionNames[i],originalCPP,originalFile + '.cpp')
                        if(len(aretheyUsed) > 0):
                            for item in headerLocations:
                                newLocationOccurrences.append(item)
                            # print(headerFunctionPositions[i])
                            newLocationOccurrences.append(extractClassName + '.h' + '-' + str(headerFunctionPositions[i]))
                            for item in aretheyUsed:
                                newLocationOccurrences.append(item)
                            tempLocationOGFile = '#' + '-' + str(currentLine)
                            newLocationOccurrences.append(tempLocationOGFile)
           
    
            if(not canFindCpp):
                continue

            functionNames,functionTypes,functionPositions = extractAllFunctionsFromClass(baseClassHeaderFile)

            # this checks to see whether there is implementation in the base class
            
            for i in range(len(functionNames)):
                fixedLocations = hasImplementationPresent(functionTypes[i],functionNames[i],baseClassSourceFile)
                if(len(fixedLocations) > 0):
                    if(canSearchOGFile):
                        aretheyUsed = checkForUsage(functionNames[i],originalCPP,originalFile + '.cpp')
                        if(len(aretheyUsed) > 0):
                            currentLineInHeader = functionPositions[i]
                            tempLocation = extractClassName + '.cpp' + '-' + fixedLocations
                            tempLocationHeader = extractClassName + '.h' +'-' + str(currentLineInHeader)
                            tempLocationOGFile = '#' + '-' + str(currentLine)
                            newLocationOccurrences.append(tempLocation)
                            newLocationOccurrences.append(tempLocationHeader)
                            newLocationOccurrences.append(tempLocationOGFile)
                            for item in aretheyUsed:
                                newLocationOccurrences.append(item)

                    #here we need to check if the shit has been implemented in the file

        currentLine += 1
    return list(set(newLocationOccurrences))

        