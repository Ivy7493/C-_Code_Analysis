from email import header
from functools import total_ordering
from pysimilar import compare
from threading import Thread #WE NEED MORE POWER BOSS


#settings
scoreThreshold = 0.85
reduceChar = ["int ", "float ", "string ", "double ", "auto ",
"char ", "const ", "static ", "vector", "()", ";", "{", "}", "->", '::']

buzzWords = ['Vector2f','Vector2', 'int', 'float','string', 'double',
            "auto"]

thresholdPoints = []

def analyze(headers,source):
    locationOccurance = []
    for x in source:
        bracketCount = 0;
        copyScope = False;
        startScope = 0;
        endScope = 0;
        currentLine = 0;
        fileScopes = []
        fileScopeSplits = []
        for line in source[x]:
            if('{' in line):
                bracketCount += 1;
                if(copyScope == False and bracketCount >= 1):
                    copyScope = True;
                    startScope = currentLine;
            if('}' in line):
                bracketCount -= 1;
                if(bracketCount == 0 and copyScope == True):
                    copyScope = False;
                    endScope = currentLine;
                    tempCounter = startScope
                    outputBlock = ""
                    while(tempCounter != endScope + 1):
                        outputBlock += source[x][tempCounter];
                        #outputBlock += '\n';
                        tempCounter += 1;
                    fileScopes.append(outputBlock)
                    fileScopeSplits.append(str(startScope) + '@' + str(endScope))

            currentLine += 1
        for y in fileScopes:
            for j in fileScopes:
                if(y != j):
                    score = compare(y,j)
                    TotalMeanSplit = 0;
                    for phrase in reduceChar:
                        TotalMeanSplit += y.count(phrase)*((len(phrase)/2))
                    fixedScore = score - TotalMeanSplit/len(y)

                    if(fixedScore > scoreThreshold):
                        #print("For ")
                        #print(y) 
                        #print(" ")
                        #print(j)
                        #print("score:", score)
                        #print("fixedScore: ", fixedScore)
                        lineIndex = fileScopes.index(y)
                        lineIndex2 = fileScopes.index(j)
                        output = x + '-' + fileScopeSplits[lineIndex]
                        output2 = x + '-' + fileScopeSplits[lineIndex2]
                        locationOccurance.append(output)
                        locationOccurance.append(output2)
    thresholdPoints = locationOccurance
    return locationOccurance;
    
def analyzeDRY(headers,source):
    #thread = Thread(target=analyze, args=(headers,source))
    #thread.start()
    #thread.join()
    test = list(set(analyze(headers,source)))
    return test
