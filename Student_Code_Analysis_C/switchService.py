from numpy import save
from implementationInheritanceService import extractImplementationTreeClassName
from persistentService import saveData,getData

def analyzeType(headers,sources):
    combined = [headers,sources]
    enumData = []
    enumNameData = []
    classNameData=[]
    classNameLocations=[]
    classScopes=[]
    for type in combined:
        for file in type:
            enumScopeCount = 0 
            for line in type[file]:
                if "enum" in line and line.find("enum")==0:
                    enumScopeCount +=1
                    counter =type[file].index(line)
                    enumProtect = False;
                    tempString = ""
                    tempList = []
                    if('{' in  line and '}' in line):
                        workingString = line[line.find("{")+1:line.rfind('}')]
                        tempList = workingString.split(',')
                    else:
                        while '}' not in type[file][counter] and enumScopeCount!=0:
                            counter+=1
                            tempString = tempString + type[file][counter]
                            if '}' in line:
                                enumScopeCount-=1
                            
                        tempString = tempString.strip('{')
                        tempStringNoScope = tempString.strip('}')
                        tempList = tempStringNoScope.split(',')

                    for enumDatum in tempList:
                        tempString = tempString.strip('{')
                        tempStringNoScope = tempString.strip('}')
                        tempDatum =enumDatum.split('=')[0]
                        tempDatum=tempDatum.strip(" ")
                        enumData.append(tempDatum)
                        enumName = ""
                        if "enum class" in line:
                            startPos = line.find("enum class") + len("enum class") + 1
                            enumName = ""
                            if(line.find("{") != -1):
                                endPos = line.find('{')
                                enumName = line[startPos:endPos]
                                enumName = enumName.strip()
                            else:
                                enumName = line[startPos:]
                                enumName = enumName.strip()
                        elif "enum" in line:
                            startPos = line.find("enum") + len("enum") + 1
                            enumName = ""
                            if(line.find("{") != -1):
                                endPos = line.find('{')
                                enumName = line[startPos:endPos]
                                enumName = enumName.strip()
                            else:
                                enumName = line[startPos:]
                                enumName = enumName.strip()
                        enumNameData.append(enumName)
                if ".h" in file and "class" in line and line.find("class") == 0 and "enum" not in line and ('{' in line or '{' in type[file][type[file].index(line)+1] or '{' in type[file][type[file].index(line)+2]):
                    
                    ###Extracting Scope
                    scopeCount = 1
                    scopeProtect = False
                    currentLine = type[file].index(line)
                    startOfClass=currentLine
                    firstOc = True;
                    while scopeCount>0:
                        if '{' in type[file][currentLine] and firstOc:
                            firstOc=False
                        elif '{' in type[file][currentLine] and not firstOc:
                            scopeCount+=1
                        if '}' in type[file][currentLine]:
                            scopeCount-=1
                        currentLine += 1
                    endOfClass = currentLine
                       
                    # Getting the classNames
                    tempClassLine = line.strip('{')
                    tempClassLine = tempClassLine.strip('}')
                    tempClassLine =tempClassLine.split(' ')[1]
                    tempClassLine=tempClassLine.strip(" ")
                    tempClassLine=tempClassLine.split(":")[0]
                    classNameLocations.append(file+"-"+str(type[file].index(line)))
                    classScopes.append(str(startOfClass)+'@'+str(endOfClass))
                    classNameData.append(tempClassLine)
    saveData("classNames",classNameData)
    saveData("classNameLocations",classNameLocations)
    saveData("classScopes",classScopes)
                    
    return enumData,enumNameData,classNameData,classNameLocations,classScopes

                        

def analyzeSwitch(file,headers,sources,typeData,fileName):
    locationOccurence = [];
    currentLine = 0;
    extractedConditions = []
    extractedLocations = []
    lastestSwitch = -1;
    for line in file:
        #Case search
        strippedLine = line.strip()
        strippedLine = strippedLine.lstrip()
        strippedLine = strippedLine.rstrip()
        if("case" in strippedLine and strippedLine.find("case") == 0 and ':' in strippedLine):
            startPos = 0;
            caseLine = ""
            if('(' in strippedLine and ')' in line and strippedLine.find(')') < strippedLine.find(':')):
                startPos = line.strip().find("(")
                endPos = line.strip().find(')')
                caseLine = line[startPos+1:endPos]
            else:
                startPos = line.strip().find(" ")
                caseLine = line[startPos+1:-1]
            if('::' in caseLine):

                caseLine = caseLine[caseLine.rfind('::')+2:]
            extractedConditions.append(caseLine)
            currenCount = currentLine
            while("switch" not in file[currenCount]  and not file[currenCount].strip().find('switch') == 0 and not file[currenCount].find('.') < file[currenCount].find("switch")):
                currenCount -=1;

            extractedLocations.append(str(currenCount))
        #declaration search
        if("switch" in line and line.strip().find('switch') == 0 and ("(" in line) and ( ")" in line) and ('=' not in line)):
            lastestSwitch = currentLine;
            startPos = line.find("(")
            counter = startPos
            while(line[counter] != ')'):
                counter+=1;
            temp = line[startPos + 1 :counter]
            tempCounter = currentLine;
            startBlock = currentLine;
            fileList = []
            fileListName = []
            if('->' in temp):
                temp = temp[temp.find('->') + 2:]
                firstReference = False;
            if('.' in temp):
                temp = temp.split('.')[0]
            try:
                extractedName = fileName.split('.')[0]
                passedFile = headers[extractedName + '.h']
                classNames=getData("classNames")
                classLocations=getData("classNameLocations")
                passedClassNames=[]
                output=[]
                for className in classNames:
                    if extractedName in classLocations[classNames.index(className)]:
                        passedClassNames.append(className)
                for passedClassName in passedClassNames:
                    output,outputlocation = extractImplementationTreeClassName(headers,sources,passedClassName,classNames,classLocations)
                    output.append(extractedName)
                types = ['.h','.cpp']
               
                for type in types:
                    for inheritance in output:
                        if type == '.cpp' and (inheritance + type) in sources :
                            try:
                                fileList.append(sources[inheritance + type])
                            except:
                                pass
                            
                        elif type == ".h" and (inheritance + type) in headers:
                            try:
                                fileList.append(headers[inheritance + type])
                            except:
                                pass
                        fileListName.append(inheritance + type)
            except:
                fileList.append(file)
            
            if(fileList == []):
                continue
            for retrievedFile in fileList:
                firstReference = False;
                for sourceLine in retrievedFile:
                    if(temp in sourceLine and (len(sourceLine) > 4 and " " in sourceLine and len(sourceLine.split(" ")) >= 2)):
                        if(( '=' in sourceLine and sourceLine.find('=') > sourceLine.find(temp) and sourceLine.find(temp) != 0) or (sourceLine.find(temp) != 0 and sourceLine[sourceLine.find(temp) + len(temp)] == ';' and "=" not in sourceLine and sourceLine.count(';') == 1) ):
                            if(not firstReference):
                                firstReference = True; 
                                cleanLine = sourceLine.rstrip();
                                startPos = 0;
                                Extracted = ""
                                if('=' not in cleanLine):
                                    workingLine = cleanLine.split(" ")
                                    Extracted = workingLine[0]
                                elif('=' in cleanLine):
                                    startPos = cleanLine.rfind("=")
                                    Extracted = cleanLine[startPos:]
                                    Extracted = Extracted.strip(" ")
                                if('::' in Extracted):
                                    tempStuff = Extracted.split('::')[1]
                                    tempStuff = tempStuff.strip(' ')
                                    tempStuff = tempStuff.strip(';')
                                    Extracted = tempStuff;
                                else:
                                    tempStuff = Extracted.strip('=')
                                    tempStuff = tempStuff.strip(' ')
                                    tempStuff = tempStuff.strip(';')
                                    Extracted = tempStuff;
                                allDataTypes = []
                                if ('<' in Extracted):
                                    workingArray = Extracted.split('<')
                                    allDataTypes.append(workingArray[0])
                                    allDataTypes.append(workingArray[1][:-1])
                                if(len(allDataTypes) == 0):
                                    allDataTypes.append(Extracted)
                                for value in allDataTypes:
                                    if(value in typeData[0]):
                                        while( '}' not in file[tempCounter]):
                                            tempCounter += 1
                                        locationOccurence.append(str(startBlock) + '@' + str(tempCounter))
                                    elif(value == "true" or value == "false"):
                                        while( '}' not in file[tempCounter]):
                                            tempCounter += 1
                                        locationOccurence.append(str(startBlock) + '@' + str(tempCounter))
                                    elif(value in typeData[1]):
                                        while( '}' not in file[tempCounter]):
                                            tempCounter += 1
                                        locationOccurence.append(str(startBlock) + '@' + str(tempCounter))
                                    
                        elif('=' in sourceLine and (sourceLine.find('=') < sourceLine.find(temp))):
                            pass

        currentLine = currentLine + 1
    if(len(extractedConditions) > 0):
        listCounter = 0
        for extracted in extractedConditions:
            if(extracted in typeData[0]):
                locationOccurence.append(extractedLocations[listCounter])
            listCounter += 1
    return locationOccurence



