def extractTypeTree(file,headers,fileName):
    #print("Current-Line: ", line)
    for line in file:
        #print(line)
        if ("private" in line or "protected" in line or "public" in line) and "class" in line and ':' in line:
            # print("YAAAAS: ", line)
            cleanline = line.split(':')[1]
            cleanline = cleanline.rstrip('}')
            cleanline = cleanline.rstrip('{')
            cleanline = cleanline.rstrip()
            cleanline = cleanline.lstrip()
            cleanline = cleanline.replace("{","")
            # print("After fixing: ")
            # print(cleanline)            
            NextInheritedClass = cleanline.split(" ")[1]
            nextInheritedHeaderFile = []
            # print("Next Inherited Class: ")
            # print(NextInheritedClass)
            try:
                #print("We trying to get ", NextInheritedClass + '.h')
                nextInheritedHeaderFile = headers[NextInheritedClass + '.h']
            except:
                print("Type got away!")
            #print("Current Level Extraction: ")
            #print("Next Class: ",NextInheritedClass)
            returnedTree,location = extractTypeTree(nextInheritedHeaderFile,headers,NextInheritedClass + '.h')
            #print("What we got back")
            #print(returnedTree)
            returnedTree.append(NextInheritedClass)
            location.append(fileName + '-' + str(file.index(line)));

            return returnedTree,location
        elif("class" in line and ':' not in line and line.index('class') == 0 and fileName.split('.')[0].lower() in line.lower()): #Here when we hit the bottom
            return [],[]


def analyzeType(headers,sources):
    combined = [headers,sources]
    enumData = []
    enumNameData = []
    classNameData=[]
    classNameLocation=[]
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
                            endPos = line.find('{')
                            enumName = line[startPos:endPos]
                            enumName = enumName.strip()
                            # print("Extracted Enum class Name: ", enumName)
                        elif "enum" in line:
                            startPos = line.find("enum") + len("enum") + 1
                            endPos = line.find('{')
                            enumName = line[startPos:endPos]
                            enumName = enumName.strip()
                            # print("Extracted Enum Name: ", enumName)
                        enumNameData.append(enumName)
                if ".h" in file and "class" in line and line.find("class") == 0 and "enum" not in line:
                    tempClassLine = line.strip('{')
                    tempClassLine = tempClassLine.strip('}')
                    tempClassLine =tempClassLine.split(' ')[1]
                    tempClassLine=tempClassLine.strip(" ")
                    tempClassLine=tempClassLine.split(":")[0]
                    classNameLocation.append(file+"-"+str(type[file].index(line)))
                    classNameData.append(tempClassLine)
                    
    return enumData,enumNameData,classNameData,classNameLocation

                        

def analyzeSwitch(file,headers,sources,typeData,fileName):
    locationOccurence = [];
    currentLine = 0;
    
    for line in file:
        if("switch" in line and ("(" in line) and ( ")" in line) and ('=' not in line) and ('{' in line or '{' in file[file.index(line) + 1])):
            print("switch found in: ",fileName)
            print(line)
            print("pos: ", str(currentLine))
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
                output,outputlocation = extractTypeTree(passedFile,headers,fileName)
                output.append(extractedName)
                types = ['.h','.cpp']
               
                for type in types:
                    for inheritance in output:
                        if type == '.cpp' and (inheritance + type) in sources :
                            try:
                                fileList.append(sources[inheritance + type])
                            except:
                                print("file ", inheritance + type, " Doesnt exist" )
                            
                        elif type == ".h" and (inheritance + type) in headers:
                            try:
                                fileList.append(headers[inheritance + type])
                            except:
                                print("file ", inheritance + type, " Doesnt exist" )
                        fileListName.append(inheritance + type)
                #print("we should look at these files")
                #print(fileListName)
            except:
                print("No header file for ", fileName)
                fileList.append(file)
            
            if(fileList == []):
                continue
            print("stage 1")
            for retrievedFile in fileList:
                firstReference = False;
                for sourceLine in retrievedFile:
                    if(temp in sourceLine and (len(sourceLine) > 4 and " " in sourceLine and len(sourceLine.split(" ")) >= 2)):
                        if(( '=' in sourceLine and sourceLine.find('=') > sourceLine.find(temp) and sourceLine.find(temp) != 0) or (sourceLine.find(temp) != 0 and sourceLine[sourceLine.find(temp) + len(temp)] == ';' and "=" not in sourceLine and sourceLine.count(';') == 1) ):
                            if(not firstReference):
                                #print("For file: " , fileListName[fileList.index(retrievedFile)])
                                print("WE found Something Cap'n!")
                                print(sourceLine)
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
                                # print("Extracted Value")
                                # print(Extracted)
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
                                #print("After Fixing")
                                #print(Extracted)
                                #print("Type data")
                                #print(typeData[0])
                                #print(typeData[1])
                                allDataTypes = []
                                if ('<' in Extracted):
                                    workingArray = Extracted.split('<')
                                    allDataTypes.append(workingArray[0])
                                    allDataTypes.append(workingArray[1][:-1])
                                if(len(allDataTypes) == 0):
                                    allDataTypes.append(Extracted)
                                for value in allDataTypes:
                                    if(value in typeData[0]):
                                        #print("YAAAS QUEEN THIS IS NOT GOOD PROGRAMMING !!!")
                                        #print('we found a switch statement on type code')
                                        while( '}' not in file[tempCounter]):
                                            tempCounter += 1
                                        locationOccurence.append(str(startBlock) + '@' + str(tempCounter))
                                    elif(value == "true" or value == "false"):
                                        #print("YAAAS QUEEN THIS IS NOT GOOD PROGRAMMING !!!")
                                        #print('we found a switch statement on type code [BOOL EDITION]')
                                        while( '}' not in file[tempCounter]):
                                            tempCounter += 1
                                        locationOccurence.append(str(startBlock) + '@' + str(tempCounter))
                                    elif(value in typeData[1]):
                                        #print("YAAAS QUEEN THIS IS NOT GOOD PROGRAMMING !!!")
                                        #print('we found a switch statement on type code [TYPE OF ENUM EDITION]')
                                        while( '}' not in file[tempCounter]):
                                            tempCounter += 1
                                        locationOccurence.append(str(startBlock) + '@' + str(tempCounter))
                                    
                        elif('=' in sourceLine and (sourceLine.find('=') < sourceLine.find(temp))):
                            print("Ignore This")

            #locationOccurence.append(str(startBlock) + '@' + str(tempCounter))
        currentLine = currentLine + 1
    return locationOccurence



