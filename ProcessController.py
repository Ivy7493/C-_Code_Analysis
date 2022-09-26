#imports for different services
from parserService import getFiles
from friendService import analyzeFriend
from globalService import analyzeGlobalVariables
from switchService import analyzeSwitch
from publicMemberService import analyzePublicMembers
from implementationInheritanceService import analyzeImplementationInheritance

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
        fileGlobalVariable,globalVariablelocation = analyzeGlobalVariables(headers[x])
        #print("Number of Global Variables: ",fileGlobalVariable)
        #print("line of Occurrences: ", globalVariablelocation)
        for member in globalVariablelocation:
            locationOccurencesForGlobal.append(x + '-' + str(member))
        GlobalGlobalCount += fileGlobalVariable


        #------------------Friend Tool------------------------------#
        fileFriendCount,fileFriendLocation = analyzeFriend(headers[x])
        #print("Number of Friend Counts: ",fileFriendCount)
        #print("Line Occurrences: ",fileFriendLocation)
        for member in fileFriendLocation:
            locationOccurrencesForFriend.append(x + '-' + str(member))
        GlobalFriendCount += fileFriendCount

        #------------------Switch Tool------------------------------#
        fileSwitchCount, fileSwitchLocation = analyzeSwitch(headers[x])
        #print("Number of switch statements: ",fileSwitchCount)
        #print("line of Occurrences: ", fileSwitchLocation)
        for member in fileSwitchLocation:
            locationOccurrencesForSwitch.append(x + '-' + str(member))
        GlobalSwitchCount += fileSwitchCount

        #------------------Public Data Member------------------------------#
        filePublicDataMember,publicDataMemberLocation = analyzePublicMembers(headers[x])
        #print("Number of Public data member declarations: ",filePublicDataMember)
        #print("line of Occurrences: ", publicDataMemberLocation)
        for member in publicDataMemberLocation:
            locationOccurrencesForPublic.append(x + '-' + str(member))
        GlobalPublicCount += filePublicDataMember

        #------------------Implementation Inheritance---------------------#
        impCount,impLine = analyzeImplementationInheritance(headers[x],source,headers)
        for member in impLine:
            locationOccurrencesForImplementationInheritance.append(member)
        GlobalImplementationInheritanceCount += impCount
        #print('implementations check:')
        #print(impCount,impLine)

    for x in source:
      
        #print('---------------------')
        #print("For File: ", x)
        #print('---------------------')

        #-----------------Global Variable tool--------------------------------------#
        fileGlobalVariable,globalVariableLocation = analyzeGlobalVariables(source[x])
        #print("Number of Global Variables: ",fileGlobalVariable)
        #print("line of Occurrences: ", globalVariableLocation)
        for member in globalVariableLocation:
            locationOccurencesForGlobal.append(x + '-' + str(member))
        GlobalGlobalCount += fileGlobalVariable

        #------------------Switch Tool------------------------------#
        fileSwitchCount, fileSwitchLocation = analyzeSwitch(source[x])
        #print("Number of switch statements: ",fileSwitchCount)
        #print("line of Occurrences: ", fileSwitchLocation)
        for member in fileSwitchLocation:
            locationOccurrencesForSwitch.append(x + '-' + str(member))
        GlobalSwitchCount += fileSwitchCount

    #-----------------------TOTAL SECTION--------------------------------#
    issueLocationArr = [list(set(locationOccurrencesForImplementationInheritance)),list(set(locationOccurencesForGlobal)),list(set(locationOccurrencesForPublic)),list(set(locationOccurrencesForSwitch)),list(set(locationOccurrencesForFriend))]
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
