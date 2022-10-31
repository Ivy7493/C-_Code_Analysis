import os #need this in order to read in infomation.

def findRawLocation(issue,rawHeaders,rawSource,source,header):
    rawLocations = []
    blackList = []
    for x in issue:
        data = x.split('-')
        workingFile = []
        lineInQuestion = ""
        endLineInQuestion = ""
        isRangeInput = False
        difference = 0
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
                difference = int(points[1]) - int(points[0])
                
            else:
                lineInQuestion = lineInQuestion[int(data[1])]
        elif('.h' in data[0]):
            workingFile = rawHeaders[data[0]]
            lineInQuestion = header[data[0]]
            if('@' in data[1]):
                isRangeInput = True
                points = data[1].split("@")
                #print("YAAAASSSS POINTS", points)
                #print("And the len of file: ", len(lineInQuestion))
                endLineInQuestion = lineInQuestion[int(points[1])]
                #print("IS this okay? ", int(points[1]))
                #print("How about this? ", lineInQuestion[int(points[1])])  
                lineInQuestion = lineInQuestion[int(points[0])] #beginning points
                difference = int(points[1]) - int(points[0])
            else:
                lineInQuestion = header[data[0]][int(data[1])] 
        counter = 0
        found = [False,False]
        pos1 = 0
        pos2 = 0
        if(isRangeInput):
            workingFileCounter = 0
            for y in workingFile:
                workingY = y.strip()
                workingY = workingY.lstrip()
                workingY = workingY.rstrip()
                commentCounter = 0;
                if(lineInQuestion in y and counter not in blackList and (workingY.find('*') != 0 and workingY.find('*/') != len(workingY) -1 and workingY.find('/*') != 0)):
                    found[0] = True
                    pos1 = counter
                    tempIndex = counter
                    blackList.append(tempIndex)
                    startingPos = pos1 + difference
                    tempIndex = startingPos
                    while endLineInQuestion not in workingFile[tempIndex]:
                        tempIndex += 1
                    found[1] = True
                    pos2 = tempIndex
                if(found[0] and found[1]):
                    #print("Check to see if this is okay?")
                    #print(data[0] + '-' + str(pos1) + '@' + str(pos2))
                    rawLocations.append(data[0] + '-' + str(pos1) + '@' + str(pos2+1))
                    break
                counter += 1
        else:
            fileCounter = 0
            for y in workingFile:
                workingY = y.strip()
                workingY = workingY.lstrip()
                workingY = workingY.rstrip()
                if(lineInQuestion in workingY and workingY.find('*') != 0 and workingY.find('*/') != len(workingY) -1 and workingY.find('/*') != 0):
                    rawLocations.append(data[0] + '-' + str(fileCounter))
                counter += 1
                fileCounter += 1;

    return rawLocations


def getFiles(path):
    # Get the list of all files and directories
    cppList = {}
    headerList = {}
    rawCppList = {}
    rawHeaderList = {}
    for (root, dirs, file) in os.walk(path):
        for f in file:
            if '.cpp' in f or '.h' in f and f.count(".") == 1 and ".html" not in f:
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