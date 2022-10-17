
def analyzeFriend(file):
    locationOccuration = []
    currentLine = 0
    underClass = False;
    scope = 0;
    for x in file:
        print("We working with line: ", x)
        if('{' in x):
            scope += 1;
        if('}' in x):
            scope -= 1;
        if("class" in x or "class " in x):
            underClass = True
        if(scope == 0):
            underClass = False;
        if (" friend " in x or "friend " in x) and (underClass) and (not x == ""):
            locationOccuration.append(currentLine)
        currentLine = currentLine + 1 #inc in order to see where the occurance of the friend occures

    return locationOccuration
