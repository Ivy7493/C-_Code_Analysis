

from operator import truediv
from sys import implementation




def analyzeImplementationInheritance(file,source,headers):
    publicCount = 0;
    scopeCount = 0;
    implementationCount = 0;
    locationOccuration =[];
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
                    #print("passed 1")
                    if('=' not in x and '0' not in x):
                        #print("passed 2")
                        isPureVirtual = False
                        cleanX = x.rstrip()
                        nextline = baseClassFile[baseClassFile.index(x)+1]
                        #print(x)
                        if(('{'in x or '}' in x)or '{' in nextline):
                            #print("passed 3")
                            locationOccuration.append(finalLine + '.h' +  "-" + str(currentLineInHeader))
                            implementationCount = implementationCount+1
                        #This section is to do with the cpp exploration of a header
                        
                        baseClassSource = source[finalLine + '.cpp'] #we now get the cpp file to see if there is a declaration in there
                        functionNameEnd = x.find('(') - 1 # we need the functions name out of the header to search for in the cpp
                        extractedName = ""
                        for y in range(functionNameEnd,0, -1):
                            if(x[y] != " "):
                                extractedName = x[y] + extractedName
                            elif(x[y] == " "):
                                break;
                        #print("Extracted function Name: ", extractedName) # the above section just extracts the function name
                        currentCppLine = 0 #variable to keep track of the current line in the cpp file
                        for y in baseClassSource: # for every line in the cpp file seach
                            if(extractedName in y and "(" in y and ")" in y): #if the function name is in the line and () are in the line, it is a function delcaration;
                                currentCppLine = baseClassSource.index(y); #Find the index of the line at which the function was found
                                #print("Found cpp Declaration at: ", currentCppLine + 1) #print it for now for debugging
                                while("}" not in baseClassSource[currentCppLine]): #While the current cpp line isnt } , we still in the delcaration
                                    #print("current Line to check:",baseClassSource[currentCppLine] )
                                    #print("Line Length: ", len(baseClassSource[currentCppLine].strip()))
                                    if((len(baseClassSource[currentCppLine].strip()) > 1 and baseClassSource[currentCppLine].strip() != "}" and baseClassSource[currentCppLine].strip() != "{") and currentCppLine != baseClassSource.index(y)):
                                        print(extractedName,"Has declaration found within in it: ", currentCppLine + 1) #if length > 1 then there is tuff in here if its not { or }
                                        locationOccuration.append(finalLine + '.h' +  "-" + str(currentLineInHeader)) #append the .h declaration location
                                        locationOccuration.append(finalLine + '.cpp' +  "-" + str(currentCppLine)) #append the .cpp declaration location
                                        implementationCount = implementationCount+1 #only inc once because of both locations count as 1 implementation
                                        break;
                                    currentCppLine = currentCppLine + 1



                           # currentCppLine = currentCppLine + 1



                            
                currentLineInHeader = currentLineInHeader+1
            return implementationCount,list(set(locationOccuration))
        
        # if(("(" not in line and ")" not in line) and ("int" in line or "double" in line or "string" in line or "auto" in line or "char" in line or "bool" in line or "float" in line) and underPublic):
        #     publicCount = publicCount + 1 #inc in the case where we find the friend keyword
        #     locationOccuration.append(currentLine)
        # currentLine= currentLine + 1;
    return 0,''