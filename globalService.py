THRESH_SHORT = 3 # minimum number of permitted characters before considered short

def analyzeGlobalVariables(file):
    currentLine = 0; #used to track the line of the file
    locationOccurations = [];
    globalCount = 0
    scopeCount = 0;
  

    for line in file:
        # Section used for rules and protections. HEctic section ahead
        if("{" in line):
            scopeCount = scopeCount + 1
        if("}" in line):
            scopeCount = scopeCount - 1
        if(('int' in line) or ('bool' in line) or ('string' in line) or ('float' in line) or ('double' in line) or ('auto' in line) or ('char' in line)):
            if(scopeCount <= 0 and (('(' not in line) or (')' not in line))):
                locationOccurations.append(currentLine)
        currentLine = currentLine + 1
    return locationOccurations