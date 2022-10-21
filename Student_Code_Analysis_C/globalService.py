THRESH_SHORT = 3 # minimum number of permitted characters before considered short

def analyzeGlobalVariables(file):
    currentLine = 0; #used to track the line of the file
    locationOccurations = [];
    scopeCount = 0;
  

    for line in file:
        # Section used for rules and protections. HEctic section ahead
        if("{" in line):
            scopeCount = scopeCount + 1
        if("}" in line):
            scopeCount = scopeCount - 1
        if(len(line) >= 4 and " " in line and (('(' not in line and ')' not in line) or ('=' in line and '(' in line)) and "#include" not in line and len(line.split(" ")) >= 2 and ("namespace" not in line)):
            if(scopeCount <= 0 and (('(' not in line) or (')' not in line))):
                locationOccurations.append(currentLine)
        currentLine = currentLine + 1
    return locationOccurations