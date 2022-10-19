
def hasImplementationInCpp(functionType,functionName,cppFile):
    #print("function Name: ", functionName)
    #print("function Type: ", functionType)
    functionStart = -1;
    implementationFound = False;
    for line in cppFile: #Run through all lines
        if((functionName in line) and (functionType in line) and ("(" in line and ")" in line )): #if we find the function okay cool
            functionStart = cppFile.index(line) #getting where it starts
            currentLine = functionStart;
            scope = 0;
            scopeProtect = True;
            while('}' not in cppFile[currentLine] and (scope != 0 or scopeProtect)):
                if(scopeProtect and "{" in cppFile[currentLine]): #used to ge through first line
                    scopeProtect = False;
                #///Deals with determining if implementation has occured in file
                if(len(cppFile[currentLine].strip()) > 1 and cppFile[currentLine].strip() != "}" and cppFile[currentLine].strip() != "{") and currentLine != cppFile.index(line):
                    implementationFound = True;

                if('{' in cppFile[currentLine]):
                    scope += 1;
                if('}' in cppFile[currentLine]):
                    scope -= 1;
                currentLine +=1;
            functionEnd = currentLine;
            if(implementationFound):
                #print("status: ", implementationFound)
                #print("range: ", str(functionStart) + '@' + str(functionEnd))
                return str(functionStart) + '@' + str(functionEnd)
    return ""
                

def hasImplementationInHeader(headerFile,fileName):
    locationOccuration = []
    for line in headerFile:
        if(("("  in line and ")" in line) and ("void" in line or "int" in line or "double" in line or "string" in line or "auto" in line or "char" in line or "bool" in line or "float" in line or "*" in line or "const" in line or "::" in line)):
            if('= 0' not in line or "=0" not in line): 
                        nextline = headerFile[headerFile.index(line)+1]
                        if(('{'in line or '}' in line)or ('{' in nextline and '(' not in nextline and ')' not in nextline)):
                            locationOccuration.append(fileName +  "-" + str(headerFile.index(line)))

    print("Location Occurs for header: ", locationOccuration)
    return locationOccuration


def extractAllFunctionsFromClass(headerFile):
    print("Name of Header: ", headerFile)
    functionNames = []
    functionTypes = []
    functionPositions = []
    for line in headerFile:
        if(("("  in line and ")" in line) and ("void" in line or "int" in line or "double" in line or "string" in line or "auto" in line or "char" in line or "bool" in line or "float" in line or "*" in line or "const" in line or "::" in line)):
            functionNameEnd = line.find('(') - 1 # we need the functions name out of the header to search for in the cpp
            extractedName = ""
            for y in range(functionNameEnd,0, -1):
                if(line[y] != " "):
                    extractedName = line[y] + extractedName
                elif(line[y] == " "):
                    break;
            print("Extracted Function Name: ",extractedName)

            #=====The following deals with extracting types from functions incase of overloading
            extractedType = ""
            extractedTypeEnd = line.find(" ")
            extractedType = line[0:extractedTypeEnd]
            #print("Type Extracted: ")
            #print(extractedType)
            if(extractedType == "virtual"):
                tempCurrentLine = ""
                counter =  extractedTypeEnd + 1
                while(line[counter] != " "):
                    tempCurrentLine = tempCurrentLine + line[counter]
                    counter+=1
                extractedType = tempCurrentLine
            functionNames.append(extractedName)
            functionTypes.append(extractedType)
            functionPositions.append(headerFile.index(line))
    return functionNames,functionTypes,functionPositions



def analyzeImplementationInheritance(file,source,headers):
    newLocationOccuration = []
    currentLine = 0
    extractClassName = ''
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
                canFindCpp = False;

            headerLocations = hasImplementationInHeader(baseClassHeaderFile,extractClassName + '.h')
            print("HeaderLocations")
            print(headerLocations)
            if(len(headerLocations) > 0):
                for x in headerLocations:
                    newLocationOccuration.append(x)
    
            if(not canFindCpp):
                continue

            functionNames,functionTypes,functionPositions = extractAllFunctionsFromClass(baseClassHeaderFile)

            # this checks to see whether there is implementation in the base class
            
            for i in range(len(functionNames)):
                fixedLocations = hasImplementationInCpp(functionTypes[i],functionNames[i],baseClassSourceFile)
                if(len(fixedLocations) > 0):
                    currentLineInHeader = functionPositions[i]
                    tempLocation = extractClassName + '.cpp' + '-' + fixedLocations
                    tempLocationHeader = extractClassName + '.h' +'-' + str(currentLineInHeader)
                    tempLocationOGFile = '#' + '-' + str(currentLine)
                    newLocationOccuration.append(tempLocation)
                    newLocationOccuration.append(tempLocationHeader)
                    newLocationOccuration.append(tempLocationOGFile)

        currentLine += 1
    return list(set(newLocationOccuration))

        