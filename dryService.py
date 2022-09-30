from email import header
from functools import total_ordering
from pysimilar import compare
from threading import Thread #WE NEED MORE POWER BOSS


#settings
scoreThreshold = 0.8
reduceChar = ["int ", "float ", "string ", "double ", "auto ",
"char ", "const ", "static ", "vector", "()", ";", "{", "}"]

thresholdPoints = []

def tempWorkSpace(headers,source):
    locationOccurance = []
    for x in source:
        print("we working with: ", x)
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
                    fileScopeSplits.append(str(startScope) + '-' + str(endScope))

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
                        print("For ")
                        print(y) 
                        print(" ")
                        print(j)
                        print("score:", score)
                        print("fixedScore: ", fixedScore)
                        lineIndex = fileScopes.index(y)
                        lineIndex2 = fileScopes.index(j)
                        output = x + '-' + fileScopeSplits[lineIndex] + '#' + fileScopeSplits[lineIndex2]
                        locationOccurance.append(output)
    print("Extracted:: ")
    print(locationOccurance)
    return locationOccurance;
                        



def analyze(headers,source):
    print("Hello")
    return tempWorkSpace(headers,source)
    source = headers
    for x in source:
        print("for file: ", x)
        fullPage = ""
        for lineX in source[x]:
                fullPage += lineX;
                fullPage += '\n';
        split1  = fullPage[:len(fullPage)//2]
        split2 = fullPage[len(fullPage)//2:]
        testscore = compare(split1,split2)
        print("Test score: ", testscore)
        pages = [split1,split2]
        TotalMeanSplit = 0
        for page in pages:
            TotalMeanSplit = 0
            TotalMeanSplit += fullPage.count("int ")*intWeight/2
            TotalMeanSplit += fullPage.count("float ")*floatWeight/2
            TotalMeanSplit += fullPage.count("string ")*stringWeight/2
            TotalMeanSplit += fullPage.count("double ")*doubleWeight/2
            TotalMeanSplit += fullPage.count("auto ")*autoWeight/2
            TotalMeanSplit += fullPage.count("char ")*charWeight/2
            TotalMeanSplit += fullPage.count("const ")*constWeight/2
            TotalMeanSplit += fullPage.count("static ")*staticWeight/2
            TotalMeanSplit += fullPage.count("vector")*VectorWeight/2
        fixedScore = testscore - TotalMeanSplit/len(fullPage)
        print("Fixed Score: ", fixedScore)

        
        continue

        for y in source:
            if(x != y):
                xLineCount = 0;
                yLineCount = 0;
                fullPage = ""
                fullPage2 = ""
                for xline in source[x]:
                    fullPage += xline;
                    fullPage += '\n';
                for yline in source[y]:
                    fullPage2 += yline
                    fullPage2 += '\n';

                Pages = [fullPage,fullPage2]
                #========>Same Page<==================#
                for page in Pages:
                    split1  = page[:len(page)//2]
                    split2 = page[len(page)//2:]
                    #print("Split 1: ", split1)
                    #print("Split 2: ", split2)
                    testscore = compare(split1,split2)
                    print("Test score: ", testscore)
                score = compare(fullPage,fullPage2);
                #print(x + " VS " + y)
                #print(score);
                variableCount1 = 0
                variableCount1 += fullPage.count("int ")*intWeight
                variableCount1 += fullPage.count("float ")*floatWeight
                variableCount1 += fullPage.count("string ")*stringWeight
                variableCount1 += fullPage.count("double ")*doubleWeight
                variableCount1 += fullPage.count("auto ")*autoWeight
                variableCount1 += fullPage.count("char ")*charWeight
                variableCount1 += fullPage.count("const ")*constWeight
                variableCount1 += fullPage.count("static ")*staticWeight

                variableCount2 = 0
                variableCount2 += fullPage2.count("int ")*intWeight
                variableCount2 += fullPage2.count("float ")*floatWeight
                variableCount2 += fullPage2.count("string ")*stringWeight
                variableCount2 += fullPage2.count("double ")*doubleWeight
                variableCount2 += fullPage2.count("auto ")*autoWeight
                variableCount2 += fullPage2.count("char ")*charWeight
                variableCount2 += fullPage2.count("const ")*constWeight
                variableCount2 += fullPage2.count("static ")*staticWeight


                reduce1 = variableCount1/len(fullPage)
                reduce2 = variableCount2/len(fullPage2)
                #print("score raw: ", score)
                score -= ((reduce1 + reduce2)/2)
                #print("weighted score: ", score)
                if(score > scoreThreshold):
                    thresholdPoints.append((x + " VS " + y + " : " + str(score)))
                    #Pseudo percentage reducation


def analyzeDRY(headers,source):
    thread = Thread(target=analyze, args=(headers,source))
    thread.start()
    thread.join()
    print(list(set(thresholdPoints)))
                
    
            
