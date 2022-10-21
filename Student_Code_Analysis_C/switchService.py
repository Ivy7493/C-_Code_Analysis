
def analyzeSwitch(file):
    locationOccuration = [];
    currentLine = 0;

    for line in file:
        if("switch" in line and ("(" in line) and ( ")" in line) and ("int" not in line and "double" not in line and "string" not in line and "auto" not in line and "char" not in line and "bool" not in line and "float" not in line) and ('=' not in line) and ('{' in line or '{' in file[file.index(line) + 1])):
            #locationOccuration.append(currentLine)
            tempCounter = currentLine;
            startBlock = currentLine;
            while( '}' not in file[tempCounter]):
                tempCounter += 1
            locationOccuration.append(str(startBlock) + '@' + str(tempCounter))
        currentLine = currentLine + 1
    return locationOccuration



