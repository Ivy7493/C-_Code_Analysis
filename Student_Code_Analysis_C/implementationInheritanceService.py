
from numpy import extract
from switchService import analyzeType

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
                        #print("Implementation found for: ",functionName)

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
        if(functionName in line and '(' in line and ')' in line and (line[line.find(functionName) + len(functionName)] == '(' or line[line.find(functionName) + len(functionName)] == ' (')):
            if('::' in line and line.find('::') < line.find(functionName) and ' ' in line and line.find(" ") < line.find('::')):
                continue
            elif '.h' in fileName and scope <= 1:
                continue
            else:
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
            returnedTree = []
            location = []
            returnedTree,location = extractImplementationTree(nextInheritedHeaderFile,headers,source,NextInheritedClass + '.h')
            #print("What we got back")
            #print(returnedTree)
            returnedTree.append(NextInheritedClass)
            location.append(fileName + '-' + str(File.index(line)));            
            return returnedTree,location
        elif("class" in line and ':' not in line): #Here when we hit the bottom
            return [],[]


def AnalyzeInheritanceChain(chain,source,headers):
    ImplementedMembers = []
    for member in chain:
        #print("We working with: ", member)
        header = []
        cpp = []

        #We gonna try get the header and cpp file
        try:
            header = headers[member + '.h']
        except:
            print("oops couldnt find header")
        try:
            cpp = source[member + '.cpp']
        except:
            print("Opps couldnt find .cpp")

        #Now that we got the  header  and cpp,  lets extract all functions from header
        if(header != []): #PS we only do this if we can actually find the header
            functionNames,functionTypes,functionPositions = extractAllFunctionsFromClass(header)
            #now we are gonna loop through all function names and only keep those with implementation
            implementedFunctions = []
            functionLocations = []
            functionFileType = []
            for function in functionNames:
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
            #Now we gonna combine the results for the inheritance object
            if(len(implementedFunctions) > 0): #PS we only wanna append something if there is something to append
                entry = {
                    'class' : member,
                    'implementedFunctions' : implementedFunctions,
                    'functionLocations' : functionLocations,
                    'fileTypes' : functionFileType
                }
                ImplementedMembers.append(entry)
    #print("Inheritance Chain")
    #print(ImplementedMembers)
    return ImplementedMembers
        

def findClassDeclaration(file,className):
    print("looking in: ",  className)
    print(file)
    className = className.lower()
    for line in file:
        fixedLine = line.lower()
        if(className in fixedLine and 'class' in fixedLine and (fixedLine.find('class') < fixedLine.find(className)) and ' ' in fixedLine and fixedLine.find('class') == 0):
            print("YEEE FOUND IT")
            return file.index(line)

def checkChainForImplementationInheritance(chain,source,headers):
    chain = chain[::-1] #reversing using list slicing
    counter = 1
    highlights = []
    linkCounter = 1
    for link in chain:
        print("For: ", link['class'])
        workingChain = chain
        linkHeader = headers[link['class'] + '.h']
        linkcpp = source[link['class'] + '.cpp']
        for i in range(counter):
            workingChain.pop(0)
        for workingLink in workingChain:
            functions = workingLink['implementedFunctions']
            functionLocations = workingLink['functionLocations']

            #print(link['class'] + ' has the function scope of : ')
            #print(functions)
            for function in functions:
                resultCPP = checkForUsage(function,linkcpp,link['class'] + '.cpp')
                resultHeader = checkForUsage(function,linkHeader,link['class'] + '.h')
                #print("Did we find Implementation?: ")
                #print(resultHeader)
               # print(resultCPP)
                for x in resultHeader:
                    highlights.append(x)
                    highlights.append(workingLink['class'] + workingLink['fileTypes'][functions.index(function)] +'-' + functionLocations[functions.index(function)])
                    line = findClassDeclaration(linkHeader, link['class'])
                    highlights.append(link['class'] + '.h' + '-' + str(line))
                
                for x in resultCPP:
                    highlights.append(x)
                    highlights.append(workingLink['class'] + workingLink['fileTypes'][functions.index(function)] + '-' + functionLocations[functions.index(function)])
                    line = findClassDeclaration(linkHeader, link['class'])
                    lineheader = findClassDeclaration(headers[workingLink['class'] + '.h'],workingLink['class'])
                    highlights.append(link['class'] + '.h' + '-' + str(line))
                    highlights.append(workingLink['class'] + '.h' + '-' + str(lineheader))
                
        counter += 1
        linkCounter+=1
    return highlights
        

def analyzeImplementationInheritance(file,source,headers,passedFileName):
    originalFile = passedFileName.split('.')[0]
    print("====================== " + passedFileName + " ======================")
    output,outputLocation = extractImplementationTree(file,headers,source,passedFileName);
    output.append(originalFile)
    preChain = AnalyzeInheritanceChain(output,source,headers)
    results = checkChainForImplementationInheritance(preChain,source,headers)
    print("This Chains Inheritance issues")
    print(results)
    print('========================================================')
    
    return list(set(results))

        