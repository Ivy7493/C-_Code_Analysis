
#imports for different services
from parserService import getFiles
from friendService import analyzeFriend
from globalService import analyzeGlobalVariables

        





def main():
    headers,source = getFiles()
    for x in headers:
        print('---------------------')
        print("For File: ", x)
        print('---------------------')

        fileFriendCount,fileFriendLocation = analyzeFriend(headers[x])
        print("Number of Friend Counts: ",fileFriendCount)
        print("Line Occurations: ",fileFriendLocation)

    for x in source:
        print('---------------------')
        print("For File: ", x)
        print('---------------------')

        fileGlobalVariable,globalVariableLocation = analyzeGlobalVariables(source[x])
        print("Number of Global Variables: ",fileGlobalVariable)
        print("line of Occurations: ", globalVariableLocation)

if __name__ == "__main__":
    main()
