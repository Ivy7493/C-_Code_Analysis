import os #need this in order to read in infomation.

def findRawLocation(issue,rawHeaders,rawSource,source,header):
    rawLocations = []
    for x in issue:
        data = x.split('-')
        workingFile = []
        lineInQuestion = ""
        if('.cpp' in data[0]):
            workingFile = rawSource[data[0]]
            lineInQuestion = source[data[0]]
            lineInQuestion = lineInQuestion[int(data[1])]
        elif('.h' in data[0]):
            workingFile = rawHeaders[data[0]]
            lineInQuestion = header[data[0]][int(data[1])] 
        counter = 0;
        for y in workingFile:
            if(lineInQuestion in y):
                rawLocations.append(data[0] + '-' + str(counter))
            counter += 1;

    return rawLocations
        




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
                for source_line in source:
                    rawSourceLines.append(source_line)
                    if('/*' in source_line):
                          code_block = True
                    if('*/' in source_line):
                           code_block = False
                    if( not code_block):
                        if("*/" in source_line):
                            source_lines.append("") # if not in code block, insert line with comments removed         
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