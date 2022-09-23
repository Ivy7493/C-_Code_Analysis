#imports for different services
from parserService import getFiles
from friendService import analyzeFriend
from globalService import analyzeGlobalVariables
from switchService import analyzeSwitch
from publicMemberService import analyzePublicMembers
from implementationInheritanceService import analyzeImplementationInheritance

def ProcessController(fileName):
    headers,source = getFiles(fileName)
    locationOccurationsForImplementationInheritance = []
    GlobalImplementationInheritanceCount = 0
    LocationOccurationsForPublic = []
    GlobalPublicCount = 0;
    LocationOccurationsForSwitch = []
    GlobalSwitchCount = 0;
    LocationOccurationsForFriend = []
    GlobalFriendCount = 0;
    LocationOccurationForGlobal = []
    GlobalGlobalCount = 0;
    for x in headers:
        print('---------------------')
        print("For File: ", x)
        print('---------------------')

        #-----------------Global Variable tool--------------------------------------#
        fileGlobalVariable,globalVariableLocation = analyzeGlobalVariables(headers[x])
        print("Number of Global Variables: ",fileGlobalVariable)
        print("line of Occurations: ", globalVariableLocation)
        for member in globalVariableLocation:
            LocationOccurationForGlobal.append(x + '-' + str(member))
        GlobalGlobalCount += fileGlobalVariable


        #------------------Friend Tool------------------------------#
        fileFriendCount,fileFriendLocation = analyzeFriend(headers[x])
        print("Number of Friend Counts: ",fileFriendCount)
        print("Line Occurations: ",fileFriendLocation)
        for member in fileFriendLocation:
            LocationOccurationsForFriend.append(x + '-' + str(member))
        GlobalFriendCount += fileFriendCount

        #------------------Switch Tool------------------------------#
        fileSwitchCount, fileSwitchLocation = analyzeSwitch(headers[x])
        print("Number of switch statements: ",fileSwitchCount)
        print("line of Occurations: ", fileSwitchLocation)
        for member in fileSwitchLocation:
            LocationOccurationsForSwitch.append(x + '-' + str(member))
        GlobalSwitchCount += fileSwitchCount

        #------------------Public Data Member------------------------------#
        filePublicDataMember,publicDataMemberLocation = analyzePublicMembers(headers[x])
        print("Number of Public data member declarations: ",filePublicDataMember)
        print("line of Occurations: ", publicDataMemberLocation)
        for member in publicDataMemberLocation:
            LocationOccurationsForPublic.append(x + '-' + str(member))
        GlobalPublicCount += filePublicDataMember

        #------------------Implementation Inheritance---------------------#
        impCount,impLine = analyzeImplementationInheritance(headers[x],source,headers)
        for member in impLine:
            locationOccurationsForImplementationInheritance.append(member)
        GlobalImplementationInheritanceCount += impCount
        print('implementations check:')
        print(impCount,impLine)

    for x in source:
      
        print('---------------------')
        print("For File: ", x)
        print('---------------------')

        #-----------------Global Variable tool--------------------------------------#
        fileGlobalVariable,globalVariableLocation = analyzeGlobalVariables(source[x])
        print("Number of Global Variables: ",fileGlobalVariable)
        print("line of Occurations: ", globalVariableLocation)
        for member in globalVariableLocation:
            LocationOccurationForGlobal.append(x + '-' + str(member))
        GlobalGlobalCount += fileGlobalVariable

        #------------------Switch Tool------------------------------#
        fileSwitchCount, fileSwitchLocation = analyzeSwitch(source[x])
        print("Number of switch statements: ",fileSwitchCount)
        print("line of Occurations: ", fileSwitchLocation)
        for member in fileSwitchLocation:
            LocationOccurationsForSwitch.append(x + '-' + str(member))
        GlobalSwitchCount += fileSwitchCount

    #-----------------------TOTAL SECTION--------------------------------#
    print(" ")
    print('=========================================================')
    locationOccurationsForImplementationInheritance = list(set(locationOccurationsForImplementationInheritance))    
    print("Total Implementation Inheritance: ")
    print ("Count: ", GlobalImplementationInheritanceCount)
    print("Occurances: ", locationOccurationsForImplementationInheritance)
    print(" ")
    print('=========================================================')
    LocationOccurationForGlobal = list(set(LocationOccurationForGlobal))
    print("Total Global Variables: ")
    print ("Count: ", GlobalGlobalCount)
    print("Occurances: ", LocationOccurationForGlobal)
    print(" ")
    print('=========================================================')
    LocationOccurationsForPublic = list(set(LocationOccurationsForPublic))
    print("Total Public Variables: ")
    print ("Count: ", GlobalPublicCount)
    print("Occurances: ", LocationOccurationsForPublic)
    print(" ")
    print('=========================================================')
    LocationOccurationsForSwitch = list(set(LocationOccurationsForSwitch))
    print("Total switch Statements: ")
    print ("Count: ", GlobalSwitchCount)
    print("Occurances: ", LocationOccurationsForSwitch)
    print(" ")
    print('=========================================================')
    LocationOccurationsForFriend = list(set(LocationOccurationsForFriend))
    print("Total Friend Statements: ")
    print ("Count: ", GlobalFriendCount)
    print("Occurances: ", LocationOccurationsForFriend)
    
    return headers,source
