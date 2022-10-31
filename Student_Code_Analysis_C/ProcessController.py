#imports for different services
from parserService import getFiles,findRawLocation
from friendService import analyzeFriend
from globalService import analyzeGlobalVariables
from switchService import analyzeSwitch,analyzeType
from publicMemberService import analyzePublicMembers
from implementationInheritanceService import analyzeImplementationInheritance
from dryService import analyzeDRY


def ProcessController(fileName):
    headers,source,rawHeaders,rawSource = getFiles(fileName)
    locationOccurrencesForImplementationInheritance = []
    locationOccurrencesForPublic = []
    locationOccurrencesForSwitch = []
    locationOccurrencesForFriend = []
    locationOccurencesForGlobal = []
    locationOccurencesForDRY = []
    # typeData = analyzeType(headers,source)
    
    typeData,enumNames,classNames,classNameLocations,classScopes = analyzeType(headers,source)
    #typeData.extend(enumNames)
    typeData = [typeData,enumNames]
    print("START OF PROCESS CONTROLLER")
    print("classNames Extracted:",classNames)
    print("Raw Line numbers of class declarations: ",classNameLocations)
    
    
    #------------------DRY TOOL---------------------------------------#
    try:
        locationOccurencesForDRY = analyzeDRY(headers,source)
    except:
        print("Dry princple errors")
    # print("First!")
    # print(locationOccurencesForDRY)
    # print('----testing Section-----')
    for currentClass in classNames:
        #------------------Implementation Inheritance---------------------#
        try:
            impLine = analyzeImplementationInheritance(source,headers,currentClass,classNames,classNameLocations,classScopes)
            if(len(impLine) != 0):
                impLine = list(set(impLine))
            for member in impLine:
                locationOccurrencesForImplementationInheritance.append(member)
        except:
            print("IMplementation error")
        
        try:
            # print("========"+ currentClass + '========')
            #print("what we passing in")
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
            print("PDM error")

    
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

        #------------------Friend Tool------------------------------#
        try:
            fileFriendLocation = analyzeFriend(headers[x])
            fileFriendLocation = list(set(fileFriendLocation))
            for member in fileFriendLocation:
                locationOccurrencesForFriend.append(x + '-' + str(member))
        except:
            print("Friend error in header")

        #------------------Switch Tool------------------------------#
        try:
            fileSwitchLocation = analyzeSwitch(headers[x],headers,source,typeData,x)
            fileSwitchLocation = list(set(fileSwitchLocation))
            for member in fileSwitchLocation:
                locationOccurrencesForSwitch.append(x + '-' + str(member))
        except:
            print("switch error")

        #------------------Public Data Member------------------------------#
       

    for x in source:
        #-----------------Global Variable tool--------------------------------------#
        try:
            
            globalVariableLocation = analyzeGlobalVariables(source[x])
            globalVariableLocation = list(set(globalVariableLocation))
            
        except:
            print("global source error")
        for member in globalVariableLocation:
            locationOccurencesForGlobal.append(x + '-' + str(member))

        #------------------Switch Tool------------------------------#
        #try:
        fileSwitchLocation = analyzeSwitch(source[x],headers,source,typeData,x)
        fileSwitchLocation = list(set(fileSwitchLocation))
        #except:
            #print("switch source error")
        for member in fileSwitchLocation:
            locationOccurrencesForSwitch.append(x + '-' + str(member))



    #======================Raw Location Test===============================#
    #print("========FULL ISSUES=====")
    #print("LOCATION OCCURENCES FOR GLOBAL",locationOccurencesForGlobal)
    rawGlobalLocations = findRawLocation(locationOccurencesForGlobal,rawHeaders,rawSource,source,headers)
    #print("global: ",rawGlobalLocations)
    rawSwitchLocations = findRawLocation(locationOccurrencesForSwitch,rawHeaders,rawSource,source,headers)
    #print("rawswitch: ",rawSwitchLocations)
    rawFriendLocations = findRawLocation(locationOccurrencesForFriend,rawHeaders,rawSource,source,headers)
    #print("rawfriend: ",rawFriendLocations)
    rawPublicLocations = findRawLocation(locationOccurrencesForPublic,rawHeaders,rawSource,source,headers)
    #print("rawpublic: ",rawPublicLocations)
    rawInheritanceLocations = findRawLocation(locationOccurrencesForImplementationInheritance,rawHeaders,rawSource,source,headers)
    #print("rawinheritance: ",rawInheritanceLocations)
    rawDRYLocations = findRawLocation(locationOccurencesForDRY,rawHeaders,rawSource,source,headers)
    #print("rawdry: ",rawDRYLocations)
    
    
    
    #-----------------------TOTAL SECTION--------------------------------#
    issueLocationArr = [list(set(rawInheritanceLocations)),list(set(rawGlobalLocations)),list(set(rawPublicLocations)),list(set(rawSwitchLocations)),list(set(rawFriendLocations)),list(set(rawDRYLocations))]
    # print('=========================================================')
    locationOccurrencesForImplementationInheritance = list(set(locationOccurrencesForImplementationInheritance))    
    # print("Total Implementation Inheritance: ")
    #print("Occurrences: ", locationOccurrencesForImplementationInheritance)
    # print(" ")
    #print('=========================================================')
    #locationOccurencesForGlobal = list(set(locationOccurencesForGlobal))
    #print("Total Global Variables: ")
    #print("Occurrences: ", locationOccurencesForGlobal)
    #print(" ")
    #print('=========================================================')
    #locationOccurrencesForPublic = list(set(locationOccurrencesForPublic))
    # print("Total Public Variables: ")
    #print("Occurrences: ", locationOccurrencesForPublic)
    # print(" ")
    # print('=========================================================')
    #locationOccurrencesForSwitch = list(set(locationOccurrencesForSwitch))
    # print("Total switch Statements: ")
    # print("Occurrences: ", locationOccurrencesForSwitch)
    # print(" ")
    # print('=========================================================')
    #locationOccurrencesForFriend = list(set(locationOccurrencesForFriend))
    # print("Total Friend Statements: ")
    # print("Occurrences: ", locationOccurrencesForFriend)
    #locationOccurencesForDRY = list(set(locationOccurencesForDRY))
    # print("Total DRY Sections: ")
    # print("Occurrences: ", locationOccurencesForDRY)
    classNameLocations=findRawLocation(classNameLocations,rawHeaders,rawSource,source,headers)
    return rawHeaders,rawSource,issueLocationArr
