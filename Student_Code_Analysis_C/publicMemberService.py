
def keywordExclusion(line):
    keywords = ["namespace","#include","#ifndef","#define","#pragma","using","template", "updates", "#if"]
    for word in keywords:
        if word in line:
            return False;
    return True;


def lengthCheck(line):
    if(len(line) >= 4 and len(line.split(" ")) >= 2):
        return True;
    else:
        return False;


def bracketCheck(line):
    if '(' not in line and ')' not in line:
        return True
    elif "(" in line and ')' in line and '=' in line and line.find("=") < line.find("("):
        return True
    else:
        return False 


def analyzePublicMembers(file):
    scopeCount = 0;
    underClass = False;
    underPublic = False;
    locationOccuration =[];
    currentLine = 0;
    roundScope = 0;
    
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
        if(("private:"in line or "protected:" in line or "private :" in line or "protected :" in line) and underClass ):
            underPublic = False;
        if('('in line):
            roundScope+=1
        if(')'in line):
            roundScope-=1
        if(lengthCheck(line) and " " in line and bracketCheck(line) and keywordExclusion(line) and underPublic and roundScope <= 0 and scopeCount <= 1):
            print("YAAAAS PUBLIC LINE: ", line )
            locationOccuration.append(currentLine)
        currentLine= currentLine + 1
    return locationOccuration