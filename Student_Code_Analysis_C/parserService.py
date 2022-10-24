import os #need this in order to read in infomation.

def findRawLocation(issue,rawHeaders,rawSource,source,header):
    rawLocations = []
    for x in issue:
        data = x.split('-')
        workingFile = []
        lineInQuestion = ""
        endLineInQuestion = ""
        isRangeInput = False
        if('.cpp' in data[0]):
            workingFile = rawSource[data[0]]
            lineInQuestion = source[data[0]]
            if('@' in data[1]):
                isRangeInput = True
                points = data[1].split("@")
                #print("YAAAASSSS POINTS", points)
                #print("And the len of file: ", len(lineInQuestion))
                endLineInQuestion = lineInQuestion[int(points[1])]
                #print("IS this okay? ", int(points[1]))
                #print("How about this? ", lineInQuestion[int(points[1])])  
                lineInQuestion = lineInQuestion[int(points[0])] #beginning points
                
            else:
                lineInQuestion = lineInQuestion[int(data[1])]
        elif('.h' in data[0]):
            workingFile = rawHeaders[data[0]]
            lineInQuestion = header[data[0]][int(data[1])] 
        counter = 0
        found = [False,False]
        pos1 = 0
        pos2 = 0
        if(isRangeInput):
            for y in workingFile:
                if(lineInQuestion in y):
                    found[0] = True
                    pos1 = counter
                    tempIndex = workingFile.index(y)
                    while(endLineInQuestion not in workingFile[tempIndex]):
                        tempIndex += 1
                    found[1] = True
                    pos2 = tempIndex
                if(found[0] and found[1]):
                    #print("Check to see if this is okay?")
                    #print(data[0] + '-' + str(pos1) + '@' + str(pos2))
                    rawLocations.append(data[0] + '-' + str(pos1) + '@' + str(pos2))
                    break
                counter += 1
        else:    
            for y in workingFile:
                if(lineInQuestion in y):
                    rawLocations.append(data[0] + '-' + str(counter))
                counter += 1

    return rawLocations
        

def parseIndents(files):
    newFiles = files
   
    for file in files:
        indentCount = 0
       # print(file)
        for x in files[file]:
            if "}" in x:
                indentCount -= 1
            if indentCount>0:
                for i in range(indentCount):
                   # print("in the x forloop and i forloop: ",x)
                    try:
                        newFiles[file][files[file].index(x)] = '$' + newFiles[file][files[file].index(x)]  #newFiles[file][files[file].index(x)]
                    except:
                        lol = 4
                        #print("That line kinda deaded")
                    #print(newFiles[file][files[file].index(x)], "printed stuff")# = '->' + newFiles[file][file.index(x)]
            if "{" in x:
                indentCount += 1
            if('case' in x and ':' in x):
                indentCount +=1
            if('break;' in x):  
                indentCount -= 1
            

    return newFiles



def getFiles(path):
    # Get the list of all files and directories
    cppList = {}
    headerList = {}
    rawCppList = {}
    rawHeaderList = {}
    for (root, dirs, file) in os.walk(path):
        for f in file:
            if '.cpp' in f or '.h' in f:
                #print(f)
                sourceFile = os.path.join(root, f)
                source = open(sourceFile, "r")
                source_lines = []
                rawSourceLines = []
                code_block = False
                inLineProtection = False
                for source_line in source:
                    rawSourceLines.append(source_line)
                    if '/*' in source_line and '*/' in source_line:
                        inLineProtection = True;
                    if '/*' in source_line:
                          code_block = True
                    if '*/' in source_line:
                           code_block = False
                    if not code_block:
                        if "*/" in source_line and not inLineProtection:
                            source_lines.append("") # if not in code block, insert line with comments removed         
                        else:
                            if inLineProtection:
                                inLineProtection = False;
                                source_lines.append(source_line.split('/*')[0].strip())
                            else:    
                                source_lines.append(source_line.split('//')[0].strip()) # if not in code block, insert line with comments removed         
                          
                #print(source_lines)
                if('.cpp' in f):
                    cppList[f]=source_lines
                    rawCppList[f]=rawSourceLines
                elif('.h' in f):
                    headerList[f]=source_lines
                    rawHeaderList[f] = rawSourceLines
                source.close()
                
    
    # for x in cppList:
    #     print(" ")
    #     print("cpp Item: ", x)
    #     for y in cppList[x]:
    #         print(y)

    # for x in headerList:
    #     print(" ")
    #     print("header Item: ", x)
    #     for y in headerList[x]:
    #         print(y)

    return headerList,cppList,rawHeaderList,rawCppList