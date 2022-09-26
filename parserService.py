import os, sys #need this in order to read in infomation.
def getFiles(path):
    # Get the list of all files and directories
    #path = os.path.dirname(__file__)
    #dir_list = os.walk(path)
    cppList = {}
    headerList = {}
    #print("Files and directories in '", path, "' :")
    for (root, dirs, file) in os.walk(path):
        for f in file:
            if '.cpp' in f:
                #print(f)
                sourceFile = os.path.join(root, f)
                source = open(sourceFile, "r")
                source_lines = []
                code_block = False
                for source_line in source:
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
                cppList[f]=source_lines
                
            elif '.h' in f:
                #print(f)
                sourceFile = os.path.join(root, f)
                source = open(sourceFile, "r")
                source_lines = []
                code_block = False
                for source_line in source:
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
                headerList[f]=source_lines
    
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

    return headerList,cppList