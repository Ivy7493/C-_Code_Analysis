

def analyzePublicMembers(file):
    publicCount = 0;
    scopeCount = 0;
    underClass = False;
    underPublic = False;
    locationOccuration =[];
    currentLine = 0;

    for line in file:
        if("{" in line): #we inc for open scope
            scopeCount = scopeCount + 1
        if("}" in line): #we dec for closed scope 
            scopeCount = scopeCount - 1
        if("class" in line): #we check to see  if one is in a class
            underClass = True; #then we set the underClass var to True
        elif(scopeCount == 0): #if scope is == 0, we cant be under class nor can be we under public
            underClass = False;
            underPublic = False;
        if("public:" in line  and underClass): #we check to see if we are in the public members of a class
            underPublic = True; #we set the under public variable to True
        if(("private:"in line or "protected:" in line) and underClass ):
            underPublic = False;
        if(("(" not in line and ")" not in line) and ("int" in line or "double" in line or "string" in line or "auto" in line or "char" in line or "bool" in line or "float" in line) and underPublic):
            publicCount = publicCount + 1 #inc in the case where we find the friend keyword
            locationOccuration.append(currentLine)
        currentLine= currentLine + 1;
    return publicCount, locationOccuration