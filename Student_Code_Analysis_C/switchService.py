def extractTypeTree(file,headers,fileName):
    #print("Current-Line: ", line)
    for line in file:
        if ("private" in line or "protected" in line or "public" in line) and "class" in line and ':' in line:
            cleanline = line.rstrip()
            lastSpacePos = cleanline.rfind(' ')
            NextInheritedClass = cleanline[lastSpacePos+1:]
            nextInheritedHeaderFile = []
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
        elif("class" in line and ':' not in line): #Here when we hit the bottom
            return [],[]


def analyzeType(headers,sources):
    combined = [headers,sources]
    enumData = []
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
    return enumData


                        

def analyzeSwitch(file,headers,sources,typeData,fileName):
    locationOccurence = [];
    currentLine = 0;
    
    for line in file:
        if("switch" in line and ("(" in line) and ( ")" in line) and ("int" not in line and "double" not in line and "string" not in line and "auto" not in line and "char" not in line and "bool" not in line and "float" not in line) and ('=' not in line) and ('{' in line or '{' in file[file.index(line) + 1])):
            print("switch found in: ",fileName)
            startPos = line.find("(")
            counter = startPos
            while(line[counter] != ')'):
                counter+=1;
            temp = line[startPos + 1 :counter]
            tempCounter = currentLine;
            startBlock = currentLine;
            if('->' in temp):
                temp = temp[temp.find('->') + 2:]
                firstReference = False;
            try:
                extractedName = fileName.split('.')[0]
                passedFile = headers[extractedName + '.h']
                output,outputlocation = extractTypeTree(passedFile,headers,fileName)
                output.append(extractedName)
                types = ['.h','.cpp']
                fileList = []
                fileListName = []
                for type in types:
                    for inheritance in output:
                        if type == '.cpp':
                            try:
                                fileList.append(sources[inheritance + type])
                            except:
                                print("file ", inheritance + type, " Doesnt exist" )
                            
                        elif type == ".h":
                            try:
                                fileList.append(headers[inheritance + type])
                            except:
                                print("file ", inheritance + type, " Doesnt exist" )
                        fileListName.append(inheritance + type)
                #print("we should look at these files")
                #print(fileListName)
            except:
                print("No header file for ", fileName)
            for retrievedFile in fileList:
                firstReference = False;
                for sourceLine in retrievedFile:
                    if(temp in sourceLine and (len(sourceLine) > 4 and " " in sourceLine and len(sourceLine.split(" ")) >= 2)):
                        if('=' in sourceLine and (sourceLine.find('=') > sourceLine.find(temp)) and sourceLine.find(temp) != 0):
                            if(not firstReference):
                                print("WE found Something Cap'n!")
                                print(sourceLine)
                                firstReference = True; 
                                cleanLine = sourceLine.rstrip();
                                startPos = cleanLine.rfind("=")
                                Extracted = cleanLine[startPos:]
                                Extracted = Extracted.strip(" ")
                                print("Extracted Value")
                                print(Extracted)
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
                                print("After Fixing")
                                print(Extracted)
                                if(Extracted in typeData):
                                    print("YAAAS QUEEN THIS IS NOT GOOD PROGRAMMING !!!")
                                    print('we found a switch statement on type code')
                                    while( '}' not in file[tempCounter]):
                                        tempCounter += 1
                                    locationOccurence.append(str(startBlock) + '@' + str(tempCounter))
                                elif(Extracted == "True" or Extracted == "False"):
                                    print("YAAAS QUEEN THIS IS NOT GOOD PROGRAMMING !!!")
                                    print('we found a switch statement on type code [BOOL EDITION]')
                                    while( '}' not in file[tempCounter]):
                                        tempCounter += 1
                                    locationOccurence.append(str(startBlock) + '@' + str(tempCounter))
                                    
                        elif('=' in sourceLine and (sourceLine.find('=') < sourceLine.find(temp))):
                            print("Ignore This")

            #locationOccurence.append(str(startBlock) + '@' + str(tempCounter))
        currentLine = currentLine + 1
    return locationOccurence



