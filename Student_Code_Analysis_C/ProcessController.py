#imports for different services
from parserService import getFiles,findRawLocation
from friendService import analyzeFriend
from globalService import analyzeGlobalVariables
from switchService import analyzeSwitch,analyzeType
from publicMemberService import analyzePublicMembers
from implementationInheritanceService import analyzeImplementationInheritance
from dryService import analyzeDRY
from persistentService import saveData,getData

def ProcessController(fileName):
    headers,source,rawHeaders,rawSource = getFiles(fileName)
    locationOccurrencesForImplementationInheritance = []
    locationOccurrencesForPublic = []
    locationOccurrencesForSwitch = []
    locationOccurrencesForFriend = []
    locationOccurencesForGlobal = []
    locationOccurencesForDRY = []
    
    typeData,enumNames,classNames,classNameLocations,classScopes = analyzeType(headers,source)
    typeData = [typeData,enumNames]
    
    saveData("processedHeaders",headers)
    saveData("processedSources",source)
    
    #------------------DRY TOOL---------------------------------------#
    try:
        locationOccurencesForDRY = analyzeDRY(headers,source)
    except:
        pass
    for currentClass in classNames:
        #------------------Implementation Inheritance---------------------#
        try:
            impLine = analyzeImplementationInheritance(source,headers,currentClass,classNames,classNameLocations,classScopes)
            if(len(impLine) != 0):
                impLine = list(set(impLine))
            for member in impLine:
                locationOccurrencesForImplementationInheritance.append(member)
        except:
            pass
        #-------------------------Public Data Member-----------------------#
        try:
            scope = classScopes[classNames.index(currentClass)];
            scope = scope.split("@")
            startPos = int(scope[0])
            endPos = int(scope[1])
            fileName = classNameLocations[classNames.index(currentClass)].split('-')[0]
            classScope = []
            if(".cpp" in fileName):
                classScope = source[fileName]
            elif(".h" in fileName):    
                classScope = headers[fileName]
            #print(classScope)
            publicDataMemberLocation = analyzePublicMembers(classScope)
            publicDataMemberLocation = list(set(publicDataMemberLocation))
            for member in publicDataMemberLocation:
                locationOccurrencesForPublic.append(classNameLocations[classNames.index(currentClass)].split('-')[0] + '-' + str(member))
        except:
            pass

          #------------------Friend Tool------------------------------#
        try:
            scope = classScopes[classNames.index(currentClass)];
            scope = scope.split("@")
            startPos = int(scope[0])
            endPos = int(scope[1])
            fileName = classNameLocations[classNames.index(currentClass)].split('-')[0]
            classScope = []
            if(".cpp" in fileName):
                classScope = source[fileName]
            elif(".h" in fileName):    
                classScope = headers[fileName]
            #classScope = classScope[startPos:endPos]
            fileFriendLocation = analyzeFriend(classScope)
            fileFriendLocation = list(set(fileFriendLocation))
            for member in fileFriendLocation:
                locationOccurrencesForFriend.append(fileName + '-' + str(member))
        except:
            print("Friend error in header")

    
    for x in headers:
        #-----------------Global Variable tool--------------------------------------#
        globalVariableLocation=[]
        try:
            globalVariableLocation = analyzeGlobalVariables(headers[x])
            globalVariableLocation = list(set(globalVariableLocation))
        except:
            print("Global error in header")
        for member in globalVariableLocation:
                locationOccurencesForGlobal.append(x + '-' + str(member))

      

        #------------------Switch Tool------------------------------#
        try:
            fileSwitchLocation = analyzeSwitch(headers[x],headers,source,typeData,x)
            fileSwitchLocation = list(set(fileSwitchLocation))
            
            for member in fileSwitchLocation:
                locationOccurrencesForSwitch.append(x + '-' + str(member))
        except:
            print("switch error")
        #print("FILE SWITCH LOCATIONS IN HEADERS :", locationOccurrencesForSwitch)

        #------------------Public Data Member------------------------------#
       

    for x in source:
        globalVariableLocation=[]
        #-----------------Global Variable tool--------------------------------------#
        try:
            
            globalVariableLocation = analyzeGlobalVariables(source[x])
            globalVariableLocation = list(set(globalVariableLocation))
            
        except:
            print("global source error")
        for member in globalVariableLocation:
            locationOccurencesForGlobal.append(x + '-' + str(member))

        #------------------Switch Tool------------------------------#
        try:
            fileSwitchLocation = analyzeSwitch(source[x],headers,source,typeData,x)
            fileSwitchLocation = list(set(fileSwitchLocation))
        
        except:
            pass
        for member in fileSwitchLocation:
            locationOccurrencesForSwitch.append(x + '-' + str(member))
 



    #======================Raw Location Test===============================#

    rawGlobalLocations = findRawLocation(locationOccurencesForGlobal,rawHeaders,rawSource,source,headers)

    rawSwitchLocations = findRawLocation(locationOccurrencesForSwitch,rawHeaders,rawSource,source,headers)

    rawFriendLocations = findRawLocation(locationOccurrencesForFriend,rawHeaders,rawSource,source,headers)

    rawPublicLocations = findRawLocation(locationOccurrencesForPublic,rawHeaders,rawSource,source,headers)

    rawInheritanceLocations = findRawLocation(locationOccurrencesForImplementationInheritance,rawHeaders,rawSource,source,headers)

    rawDRYLocations = findRawLocation(locationOccurencesForDRY,rawHeaders,rawSource,source,headers)

    
    
    #-----------------------TOTAL SECTION--------------------------------#
    issueLocationArr = [list(set(rawInheritanceLocations)),list(set(rawGlobalLocations)),list(set(rawPublicLocations)),list(set(rawSwitchLocations)),list(set(rawFriendLocations)),list(set(rawDRYLocations))]
    locationOccurrencesForImplementationInheritance = list(set(locationOccurrencesForImplementationInheritance))    
    classNameLocations=findRawLocation(classNameLocations,rawHeaders,rawSource,source,headers)
    
    return rawHeaders,rawSource,issueLocationArr
