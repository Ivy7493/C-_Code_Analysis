
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


def extractImplementationTree(File, headers, source, fileName):
    #print("For file: ", fileName)
    for line in File:
        #print("Current-Line: ", line)
        if(("private"in line or "protected" in line or "public" in line) and "class" in line and ':' in line):
            #print("YAAAAS: ", line)
            cleanline = line.rstrip()
            lastSpacePos = cleanline.rfind(' ')
            NextInheritedClass = cleanline[lastSpacePos+1:]
            try:
                #print("We trying to get ", NextInheritedClass + '.h')
                nextInheritedHeaderFile = headers[NextInheritedClass + '.h']
            except:
                print("Bugger it got away!")
            #print("Current Level Extraction: ")
            #print("Next Class: ",NextInheritedClass)
            returnedTree,location = extractImplementationTree(nextInheritedHeaderFile,headers,source,NextInheritedClass + '.h')
            #print("What we got back")
            #print(returnedTree)
            returnedTree.append(NextInheritedClass)
            location.append(fileName + '-' + str(File.index(line)));
            
            return returnedTree,location
        elif("class" in line and ':' not in line): #Here when we hit the bottom
            return [],[]





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



    output,outputLocation = extractImplementationTree(file,headers,source,passedFileName);
    print("=========REEEEEEEEEEEEEE ==========")
    print(outputLocation)
    output.append(originalFile)
    globalInheritanceList = []
    globalFileName = []
    globalInheritanceListLocations = []
    protect = True
    print("The Tree we got back: ", output)

    if(len(output) == 1):
        return []
    for node in output:
        print("Current Node: ", node)
        nodeHeader =[]
        nodeCPP = []
        try:
            nodeHeader = headers[node + '.h']
        except:
            print("Couldnt Find Node Header: ", node)
        try:
            nodeCPP = source[node + '.cpp']
        except:
            print("Couldnt Find Node Source: ", node)
        if(nodeHeader != []):
            functionNames,functionTypes,functionPositions = extractAllFunctionsFromClass(nodeHeader)

            #=========================NEEDS TO BE FIXED===========================#
            if(output.index(node)  == len(output) - 1):
                baseFunctionNames, baseFunctionTypes, baseFunctionPositions = extractAllFunctionsFromClass(headers[output[0] + '.h'])
                print("Used Functions: ", globalInheritanceList)
                print("extracted functions: ", baseFunctionNames )
                for usedFunction in globalInheritanceList:
                    if usedFunction in baseFunctionNames:
                        print(usedFunction, " is present");
                        isImplementedCpp = hasImplementationPresent(" ", usedFunction, source[output[0] + '.cpp'])
                        if(len(isImplementedCpp) > 0):
                            print("Current Outputs!")
                            print(output[0])
                            newLocationOccurrences.append(output[0] + '.cpp' + '-' + isImplementedCpp)
                            newLocationOccurrences.append(output[0] + '.h' + '-' + str(baseFunctionPositions[baseFunctionNames.index(usedFunction)]))
            #======================================================================#
            
            if(protect):
                print("First run")
                protect = False;
            elif len(globalInheritanceList) > 0 and protect==False and nodeCPP != []:
                for function in globalInheritanceList:
                    resultCPP = checkForUsage(function,nodeCPP,node + '.cpp')
                    resultHeader = checkForUsage(function,nodeHeader,node + '.h')
                    if(len(resultCPP) > 0):
                        #print("What we appending: ")
                        #print(str(outputLocation[output.index(node)]))
                        newLocationOccurrences.append(str(outputLocation[output.index(node) - 1]))
                        #newLocationOccurrences.append(globalFileName[globalInheritanceList.index(function) - 1] + '-' + str(globalInheritanceListLocations[globalInheritanceList.index(function) - 1]))
                        for issue in resultCPP:
                            newLocationOccurrences.append(issue)  
                    if(len(resultHeader) > 0):
                        #print("What we appending: ")
                        #print(str(outputLocation[output.index(node)]))
                        newLocationOccurrences.append(str(outputLocation[output.index(node) -1]))
                        #newLocationOccurrences.append(globalFileName[globalInheritanceList.index(function) - 1] + '-' + str(globalInheritanceListLocations[globalInheritanceList.index(function) - 1]))

                        #print("SAFE !")
                        for issue in resultHeader:
                            newLocationOccurrences.append(issue)
                    #print("And for the function declaration: ")
                    #print(globalFileName[globalInheritanceList.index(function)] + '-' + str(globalInheritanceListLocations[globalInheritanceList.index(function)]))
                    #newLocationOccurrences.append(globalFileName[globalInheritanceList.index(function)] + '-' + str(globalInheritanceListLocations[globalInheritanceList.index(function)]))
                    
                
            for i in range(len(functionNames)):
                if len(hasImplementationPresent(functionTypes[i],functionNames[i],nodeHeader)) > 0:
                    print("YES we found some implementation in header", functionNames[i])
                    globalInheritanceList.append(functionNames[i])
                    globalInheritanceListLocations.append(functionPositions[i])
                    globalFileName.append(node + '.h')

                elif len(hasImplementationPresent(functionTypes[i],functionNames[i], nodeCPP)) > 0:
                    print("YES we found some implementation in CPP", functionNames[i])
                    globalInheritanceList.append(functionNames[i])
                    globalInheritanceListLocations.append(functionPositions[i])
                    globalFileName.append(node + '.cpp')
        holder = []
       
    #print("What we returning: ", list(set(newLocationOccurrences)))
    return list(set(newLocationOccurrences))


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
                            print(headerFunctionPositions[i])
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

        