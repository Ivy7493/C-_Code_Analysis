#imports for different services
from parserService import getFiles,findRawLocation
from friendService import analyzeFriend
from globalService import analyzeGlobalVariables
from switchService import analyzeSwitch
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

    #------------------DRY TOOL---------------------------------------#
    locationOccurencesForDRY = analyzeDRY(headers,source)
    for x in headers:
        #-----------------Global Variable tool--------------------------------------#
        try:
            globalVariableLocation = []
            globalVariablelocation = analyzeGlobalVariables(headers[x])
            globalVariablelocation = list(set(globalVariableLocation))
            for member in globalVariablelocation:
                locationOccurencesForGlobal.append(x + '-' + str(member))
        except:
            print("global error")

        #------------------Friend Tool------------------------------#
        try:
            fileFriendLocation = analyzeFriend(headers[x])
            fileFriendLocation = list(set(fileFriendLocation))
            for member in fileFriendLocation:
                locationOccurrencesForFriend.append(x + '-' + str(member))
        except:
            print("global error")

        #------------------Switch Tool------------------------------#
        try:
            fileSwitchLocation = analyzeSwitch(headers[x])
            fileSwitchLocation = list(set(fileSwitchLocation))
            for member in fileSwitchLocation:
                locationOccurrencesForSwitch.append(x + '-' + str(member))
        except:
            print("switch error")

        #------------------Public Data Member------------------------------#
        try:
            publicDataMemberLocation = analyzePublicMembers(headers[x])
            publicDataMemberLocation = list(set(publicDataMemberLocation))
            for member in publicDataMemberLocation:
                locationOccurrencesForPublic.append(x + '-' + str(member))
        except:
            print("PDM error")

        #------------------Implementation Inheritance---------------------#
        try:
            impLine = analyzeImplementationInheritance(headers[x],source,headers)
            jcounter = 0;
            for j in impLine:
                if '#' in j:
                    impLine[jcounter] = impLine[jcounter].replace('#', x)
                jcounter += 1;

            impLine = list(set(impLine))
        except:
            print("Implementation Error")
        for member in impLine:
            locationOccurrencesForImplementationInheritance.append(member)

   
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
        try:
            fileSwitchLocation = analyzeSwitch(source[x])
            fileSwitchLocation = list(set(fileSwitchLocation))
        except:
            print("switch source error")
        for member in fileSwitchLocation:
            locationOccurrencesForSwitch.append(x + '-' + str(member))



    #======================Raw Location Test===============================#
    rawGlobalLocations = findRawLocation(locationOccurencesForGlobal,rawHeaders,rawSource,source,headers)
    rawSwitchLocations = findRawLocation(locationOccurrencesForSwitch,rawHeaders,rawSource,source,headers)
    rawFriendLocations = findRawLocation(locationOccurrencesForFriend,rawHeaders,rawSource,source,headers)
    rawPublicLocations = findRawLocation(locationOccurrencesForPublic,rawHeaders,rawSource,source,headers)
    rawInheritanceLocations = findRawLocation(locationOccurrencesForImplementationInheritance,rawHeaders,rawSource,source,headers)
    #print("====================HERE=====================")
    #print(list(set(rawInheritanceLocations)))

    #-----------------------TOTAL SECTION--------------------------------#
    issueLocationArr = [list(set(rawInheritanceLocations)),list(set(rawGlobalLocations)),list(set(rawPublicLocations)),list(set(rawSwitchLocations)),list(set(rawFriendLocations))]
    print('=========================================================')
    locationOccurrencesForImplementationInheritance = list(set(locationOccurrencesForImplementationInheritance))    
    #print("Total Implementation Inheritance: ")
    #print("Occurrences: ", locationOccurrencesForImplementationInheritance)
    #print(" ")
    #print('=========================================================')
    locationOccurencesForGlobal = list(set(locationOccurencesForGlobal))
    #print("Total Global Variables: ")
    #print("Occurrences: ", locationOccurencesForGlobal)
    #print(" ")
    #print('=========================================================')
    locationOccurrencesForPublic = list(set(locationOccurrencesForPublic))
    #print("Total Public Variables: ")
    #print("Occurrences: ", locationOccurrencesForPublic)
    #print(" ")
    #print('=========================================================')
    locationOccurrencesForSwitch = list(set(locationOccurrencesForSwitch))
    #print("Total switch Statements: ")
    #print("Occurrences: ", locationOccurrencesForSwitch)
    #print(" ")
    #print('=========================================================')
    locationOccurrencesForFriend = list(set(locationOccurrencesForFriend))
    #print("Total Friend Statements: ")
    #print("Occurrences: ", locationOccurrencesForFriend)
    return rawHeaders,rawSource,issueLocationArr
