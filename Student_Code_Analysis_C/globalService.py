THRESH_SHORT = 3 # minimum number of permitted characters before considered short


def keywordExclusion(line):
    keywords = ["namespace","#include","#ifndef","#define","#pragma","using","template", "updates", "#if", '#']
    for word in keywords:
        if word in line:
            return False;
    return True;

def bracketCheck(line,file):
    print("bracketcheck***************************:",file[file.index(line)+1])
    if '(' in line and ')' in line and ('{' not in line and '{' not in file[file.index(line)+1] and '{' not in file[file.index(line)+2]):
        return True
    elif "(" in line and ')' in line or "(" in line and ")":
        return False
    elif ")" in line and '(' not in line and "{" in file[file.index[line] + 1]:
        return False;
    else:
        return True

def classCheck(line,scope,file):
    if "class" in line and line.find("class") == 0 or ("class" in file[file.index(line) - 1] and file[file.index(line) - 1].find("class") == 0):
        return False
    else:
        return True
    
def analyzeGlobalVariables(file):
    currentLine = 0; #used to track the line of the file
    locationOccurences = [];
    scopeCount = 0;
    for line in file:
        # Section used for rules and protections. HEctic section ahead
        # print("HERE IN GLOBAL VARIABLE",line)
        if("{" in line):
            scopeCount = scopeCount + 1
        if("}" in line):
            scopeCount = scopeCount - 1
        if len(line) >= 4 and " " in line and bracketCheck(line,file) and len(line.split(" ")) >= 2 and keywordExclusion(line) and classCheck(line,scopeCount,file):
            if scopeCount <= 0:
                print("PASSED GLOBAL VARIABLE TOOL we found a global variable in: ", line)
                locationOccurences.append(currentLine)
        currentLine = currentLine + 1
    print("IN GLOBAL==========",locationOccurences,"=================")
    return locationOccurences