

def analyzeSwitch(file):
    locationOccuration = [];
    currentLine = 0;

    for line in file:
        if("switch" in line and ("(" in line or ")" in line) and ("int" not in line and "double" not in line and "string" not in line and "auto" not in line and "char" not in line and "bool" not in line and "float" not in line) and ('=' not in line)):
            locationOccuration.append(currentLine)
        currentLine = currentLine + 1
    return locationOccuration


