

def analyzePublicMembers(file):
    publicCount = 0;
    scopeCount = 0;
    underClass = False;
    underPublic = False;

    for line in file:
        if("class" in line): #we check to see  if one is in a class
            underClass = True; #then we set the underClass var to True
        if("public" in line  and underClass): #we check to see if we are in the public members of a class
            underPublic = True; #we set the under public variable to True
        if("{" in line): #we inc for open scope
            scopeCount = scopeCount + 1
        if("}" in line): #we dec for closed scope 
            scopeCount = scopeCount - 1
            if(scopeCount == 0): #if scope is == 0, we cant be under class nor can be we under public
                underClass = False;
                underPublic = False;
        

