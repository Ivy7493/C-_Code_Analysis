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
    GlobalGlobalCount = 0;
    for x in headers:
        #-----------------Global Variable tool--------------------------------------#
        try:
            globalVariableLocation = []
            globalVariablelocation = analyzeGlobalVariables(headers[x])
            globalVariablelocation = list(set(globalVariableLocation))
            fileGlobalVariable = len(globalVariablelocation)
            for member in globalVariablelocation:
                locationOccurencesForGlobal.append(x + '-' + str(member))
        except:
            print("global error")

        #------------------Friend Tool------------------------------#
        try:
            fileFriendLocation = analyzeFriend(headers[x])
            fileFriendLocation = list(set(fileFriendLocation))
            fileFriendCount = len(fileFriendLocation)
            for member in fileFriendLocation:
                locationOccurrencesForFriend.append(x + '-' + str(member))
        except:
            print("global error")

        #------------------Switch Tool------------------------------#
        try:
            fileSwitchLocation = analyzeSwitch(headers[x])
            fileSwitchLocation = list(set(fileSwitchLocation))
            fileSwitchCount = len(fileSwitchLocation)
            for member in fileSwitchLocation:
                locationOccurrencesForSwitch.append(x + '-' + str(member))
        except:
            print("switch error")

        #------------------Public Data Member------------------------------#
        try:
            publicDataMemberLocation = analyzePublicMembers(headers[x])
            publicDataMemberLocation = list(set(publicDataMemberLocation))
            filePublicDataMember = len(publicDataMemberLocation)
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
            impCount = len(impLine)
        except:
            print("Implementation Error")
        for member in impLine:
            locationOccurrencesForImplementationInheritance.append(member)

        #------------------DRY TOOL---------------------------------------#
    print('---->1')
    locationOccurencesForDRY = analyzeDRY(headers,source)
    print('---->2')
    for x in source:
      
        #print('---------------------')
        #print("For File: ", x)
        #print('---------------------')

        #-----------------Global Variable tool--------------------------------------#
        try:
            globalVariableLocation = analyzeGlobalVariables(source[x])
            globalVariableLocation = list(set(globalVariableLocation))
            fileGlobalVariable = len(globalVariableLocation)
        except:
            print("global source error")
        for member in globalVariableLocation:
            locationOccurencesForGlobal.append(x + '-' + str(member))

        #------------------Switch Tool------------------------------#
        try:
            fileSwitchLocation = analyzeSwitch(source[x])
            fileSwitchLocation = list(set(fileSwitchLocation))
            fileSwitchCount = len(fileSwitchLocation)
            #print("Number of switch statements: ",fileSwitchCount)
            #print("line of Occurrences: ", fileSwitchLocation)
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
    print("====================HERE=====================")
    print(list(set(rawInheritanceLocations)))

    #-----------------------TOTAL SECTION--------------------------------#
    issueLocationArr = [list(set(locationOccurrencesForImplementationInheritance)),locationOccurencesForGlobal,list(set(locationOccurrencesForPublic)),list(set(locationOccurrencesForSwitch)),list(set(locationOccurrencesForFriend))]
    issueCountArr = [len(list(set(locationOccurrencesForImplementationInheritance))),len(list(set(locationOccurencesForGlobal))),len(list(set(locationOccurrencesForPublic))),len(list(set(locationOccurrencesForSwitch))),len(list(set(locationOccurrencesForFriend)))]
    print(" ")
    print('=========================================================')
    locationOccurrencesForImplementationInheritance = list(set(locationOccurrencesForImplementationInheritance))    
    print("Total Implementation Inheritance: ")
    print("Occurrences: ", locationOccurrencesForImplementationInheritance)
    print(" ")
    print('=========================================================')
    locationOccurencesForGlobal = list(set(locationOccurencesForGlobal))
    print("Total Global Variables: ")
    print("Occurrences: ", locationOccurencesForGlobal)
    print(" ")
    print('=========================================================')
    locationOccurrencesForPublic = list(set(locationOccurrencesForPublic))
    print("Total Public Variables: ")
    print("Occurrences: ", locationOccurrencesForPublic)
    print(" ")
    print('=========================================================')
    locationOccurrencesForSwitch = list(set(locationOccurrencesForSwitch))
    print("Total switch Statements: ")
    print("Occurrences: ", locationOccurrencesForSwitch)
    print(" ")
    print('=========================================================')
    locationOccurrencesForFriend = list(set(locationOccurrencesForFriend))
    print("Total Friend Statements: ")
    print("Occurrences: ", locationOccurrencesForFriend)
    
    return headers,source,issueCountArr,issueLocationArr
