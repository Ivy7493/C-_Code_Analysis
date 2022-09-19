THRESH_SHORT = 3 # minimum number of permitted characters before considered short

def analyzeGlobalVariables(file):
    underPublic = False; #used as protections to bypass checks for the bad variables
    underScope = False; # ^ ^
    specialCase = False; #Used in special cases, eg what if {} occurs in the same line?
    currentLine = 0; #used to track the line of the file
    locationOccurations = [];
    gobalCount = 0
    print('QUEEEN') #YAAAAAAS
    print(file)




    #
    var_names = 0
    var_names_short = 0
    for_loops = 0
    for_loops_scoped = 0
 
    for line in file:
        # Section used for rules and protections. HEctic section ahead
        if("{" in line):
            underScope = True
        if("}" in line):
            underScope = False;
            if(underPublic): #this exits to turn off the under public incase there is no private: field
                underPublic = False;
        if("{" in line and "}" in line):
            specialCase = True;
        if("public:" in line):
            underPublic = True
        if("private:" in line):
            underPublic = False
        

        

        temp = line.split(' ')
        if len(temp) >= 1:
            if temp[0] == 'int' or temp[0] == 'double' or temp[0] == 'float' or temp[0] == 'bool' or temp[0] == 'char' or temp[0] == 'string' or temp[0]=='auto':
                if(underPublic and not "()" in line):
                   print("")
                elif(not specialCase and not underScope and not underPublic):
                    globalCount = globalCount + 1;
                    locationOccurations.append(currentLine)
                
                var_names += 1
                if len(temp[1]) < THRESH_SHORT:
                    var_names_short += 1
        # Check scoping on loops
        if 'for' in line:
            for_loops += 1
            if 'int' in line or 'auto' in line or 'decltype' in line:
                for_loops_scoped += 1
                # Step 3: Print final report
    currentLine = currentLine + 1
    print("Total Short Variable Names: " + str(var_names_short) + " out of " + str(var_names) + " considered")
    print("Total Scoping Issues: " + str(for_loops - for_loops_scoped) + " out of " + str(for_loops) + " considered")