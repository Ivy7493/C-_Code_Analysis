#imports for different services
from parserService import getFiles
from friendService import analyzeFriend
from globalService import analyzeGlobalVariables
from switchService import analyzeSwitch
from publicMemberService import analyzePublicMembers
from implementationInheritanceService import analyzeImplementationInheritance
from dryService import analyzeDRY

def ProcessController(fileName):
    headers,source = getFiles(fileName)
    locationOccurrencesForImplementationInheritance = []
    GlobalImplementationInheritanceCount = 0
    locationOccurrencesForPublic = []
    GlobalPublicCount = 0;
    locationOccurrencesForSwitch = []
    GlobalSwitchCount = 0;
    locationOccurrencesForFriend = []
    GlobalFriendCount = 0;
    locationOccurencesForGlobal = []
    GlobalGlobalCount = 0;
    for x in headers:
        #print('---------------------')
        #print("For File: ", x)
        #print('---------------------')

        #-----------------Global Variable tool--------------------------------------#
        globalVariableLocation = []
        globalVariablelocation = analyzeGlobalVariables(headers[x])
        globalVariablelocation = list(set(globalVariableLocation))
        fileGlobalVariable = len(globalVariablelocation)
        for member in globalVariablelocation:
            locationOccurencesForGlobal.append(x + '-' + str(member))
        GlobalGlobalCount += fileGlobalVariable

        #------------------Friend Tool------------------------------#
        fileFriendLocation = analyzeFriend(headers[x])
        fileFriendLocation = list(set(fileFriendLocation))
        fileFriendCount = len(fileFriendLocation)
        for member in fileFriendLocation:
            locationOccurrencesForFriend.append(x + '-' + str(member))
        GlobalFriendCount += fileFriendCount

        #------------------Switch Tool------------------------------#
        fileSwitchLocation = analyzeSwitch(headers[x])
        fileSwitchLocation = list(set(fileSwitchLocation))
        fileSwitchCount = len(fileSwitchLocation)
        for member in fileSwitchLocation:
            locationOccurrencesForSwitch.append(x + '-' + str(member))
        GlobalSwitchCount += fileSwitchCount

        #------------------Public Data Member------------------------------#
        publicDataMemberLocation = analyzePublicMembers(headers[x])
        publicDataMemberLocation = list(set(publicDataMemberLocation))
        filePublicDataMember = len(publicDataMemberLocation)
        for member in publicDataMemberLocation:
            locationOccurrencesForPublic.append(x + '-' + str(member))
        GlobalPublicCount += filePublicDataMember

        #------------------Implementation Inheritance---------------------#
        try:
            impLine = analyzeImplementationInheritance(headers[x],source,headers)
            impLine = list(set(impLine))
            impCount = len(impLine)
        except:
            print("Implementation Error")
        for member in impLine:
            locationOccurrencesForImplementationInheritance.append(member)
        GlobalImplementationInheritanceCount += impCount

        #------------------DRY TOOL---------------------------------------#
    print('---->1')
    locationOccurencesForDRY = analyzeDRY(headers,source)
    print('---->2')
    for x in source:
      
        #print('---------------------')
        #print("For File: ", x)
        #print('---------------------')

        #-----------------Global Variable tool--------------------------------------#
        globalVariableLocation = analyzeGlobalVariables(source[x])
        globalVariableLocation = list(set(globalVariableLocation))
        fileGlobalVariable = len(globalVariableLocation)
        for member in globalVariableLocation:
            locationOccurencesForGlobal.append(x + '-' + str(member))
        GlobalGlobalCount += fileGlobalVariable

        #------------------Switch Tool------------------------------#
        fileSwitchLocation = analyzeSwitch(source[x])
        fileSwitchLocation = list(set(fileSwitchLocation))
        fileSwitchCount = len(fileSwitchLocation)
        #print("Number of switch statements: ",fileSwitchCount)
        #print("line of Occurrences: ", fileSwitchLocation)
        for member in fileSwitchLocation:
            locationOccurrencesForSwitch.append(x + '-' + str(member))
        GlobalSwitchCount += fileSwitchCount

    #-----------------------TOTAL SECTION--------------------------------#
    issueLocationArr = [list(set(locationOccurrencesForImplementationInheritance)),locationOccurencesForGlobal,list(set(locationOccurrencesForPublic)),list(set(locationOccurrencesForSwitch)),list(set(locationOccurrencesForFriend))]
    issueCountArr = [GlobalImplementationInheritanceCount,GlobalGlobalCount,GlobalPublicCount,GlobalSwitchCount,GlobalFriendCount]
    # print(" ")
    # print('=========================================================')
    # locationOccurrencesForImplementationInheritance = list(set(locationOccurrencesForImplementationInheritance))    
    # print("Total Implementation Inheritance: ")
    # print ("Count: ", GlobalImplementationInheritanceCount)
    # print("Occurrences: ", locationOccurrencesForImplementationInheritance)
    # print(" ")
    # print('=========================================================')
    # LocationOccurencesForGlobal = list(set(LocationOccurencesForGlobal))
    # print("Total Global Variables: ")
    # print ("Count: ", GlobalGlobalCount)
    # print("Occurrences: ", LocationOccurencesForGlobal)
    # print(" ")
    # print('=========================================================')
    # LocationOccurrencesForPublic = list(set(LocationOccurrencesForPublic))
    # print("Total Public Variables: ")
    # print ("Count: ", GlobalPublicCount)
    # print("Occurrences: ", LocationOccurrencesForPublic)
    # print(" ")
    # print('=========================================================')
    # LocationOccurrencesForSwitch = list(set(LocationOccurrencesForSwitch))
    # print("Total switch Statements: ")
    # print ("Count: ", GlobalSwitchCount)
    # print("Occurrences: ", LocationOccurrencesForSwitch)
    # print(" ")
    # print('=========================================================')
    # LocationOccurrencesForFriend = list(set(LocationOccurrencesForFriend))
    # print("Total Friend Statements: ")
    # print ("Count: ", GlobalFriendCount)
    # print("Occurrences: ", LocationOccurrencesForFriend)
    return headers,source,issueCountArr,issueLocationArr
