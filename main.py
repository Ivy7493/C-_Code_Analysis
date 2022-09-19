
from distutils import extension
import os, sys #need this in order to read in infomation.




def getFiles():
    # Get the list of all files and directories
    path = os.path.dirname(__file__)
    #dir_list = os.walk(path)
    cppList = []
    headerList = []
    print("Files and directories in '", path, "' :")
    for (root, dirs, file) in os.walk(path):
        for f in file:
            if '.cpp' in f:
                cppList.append(f)
                print(f)
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
                          source_lines.append(source_line.split('//')[0].strip()) # if not in code block, insert line with comments removed
                            
                print(source_lines)
            elif '.h' in f:
                headerList.append(f)
                print(f)
    print("header List: ", headerList)
    print("cpp List: ", cppList)

    return headerList,cppList
        




getFiles();