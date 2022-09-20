
#imports for different services
from parserService import getFiles
from friendService import analyzeFriend
from globalService import analyzeGlobalVariables
from switchService import analyzeSwitch

        





def main():
    headers,source = getFiles()
    for x in headers:
        print('---------------------')
        print("For File: ", x)
        print('---------------------')

        fileFriendCount,fileFriendLocation = analyzeFriend(headers[x])
        print("Number of Friend Counts: ",fileFriendCount)
        print("Line Occurations: ",fileFriendLocation)


        fileSwitchCount, fileSwitchLocation = analyzeSwitch(headers[x])
        print("Number of switch statements: ",fileSwitchCount)
        print("line of Occurations: ", fileSwitchLocation)

    for x in source:
        print('---------------------')
        print("For File: ", x)
        print('---------------------')

        fileGlobalVariable,globalVariableLocation = analyzeGlobalVariables(source[x])
        print("Number of Global Variables: ",fileGlobalVariable)
        print("line of Occurations: ", globalVariableLocation)


        fileSwitchCount, fileSwitchLocation = analyzeSwitch(source[x])
        print("Number of switch statements: ",fileSwitchCount)
        print("line of Occurations: ", fileSwitchLocation)


if __name__ == "__main__":
    main()
