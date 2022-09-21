

from operator import truediv
from sys import implementation




def analyzeImplementationInheritance(file,source,headers):
    publicCount = 0;
    scopeCount = 0;
    implementationCount = 0;
    locationOccurationHeader =[];
    currentLine = 0;
    finalLine = ''
    baseClassFile =[]
    isPureVirtual = True;
    for line in file:
        if(("private"in line or "protected" in line or "public" in line) and "class" in line):
            cleanline = line.rstrip()
            lastSpacePos = cleanline.rfind(' ')
            finalLine = cleanline[lastSpacePos+1:]
            print('Class is inherited from', finalLine)
            baseClassFile = headers[finalLine+'.h']
            currentLineInHeader = 0;
            for x in baseClassFile:
                # if( 'virtual' in x and '=' in x and '0' in x):
                if(("("  in x and ")" in x) and ("void" in x or "int" in x or "double" in x or "string" in x or "auto" in x or "char" in x or "bool" in x or "float" in x)):
                    print("passed 1")
                    if('=' not in x and '0' not in x):
                        print("passed 2")
                        isPureVirtual = False
                        cleanX = x.rstrip()
                        nextline = baseClassFile[baseClassFile.index(x)+1]
                        print(x)
                        if(('{'in x or '}' in x)or '{' in nextline):
                            print("passed 3")
                            locationOccurationHeader.append(currentLineInHeader)
                            implementationCount = implementationCount+1
                            
                currentLineInHeader = currentLineInHeader+1
            return implementationCount,locationOccurationHeader
        
        # if(("(" not in line and ")" not in line) and ("int" in line or "double" in line or "string" in line or "auto" in line or "char" in line or "bool" in line or "float" in line) and underPublic):
        #     publicCount = publicCount + 1 #inc in the case where we find the friend keyword
        #     locationOccuration.append(currentLine)
        # currentLine= currentLine + 1;
    return 0,''