import unittest

from numpy import append
from parserService import getFiles
from friendService import analyzeFriend
from globalService import analyzeGlobalVariables
from switchService import analyzeSwitch
from publicMemberService import analyzePublicMembers
from implementationInheritanceService import analyzeImplementationInheritance
from parserService import getFiles
import os

class TestClass(unittest.TestCase):

    #==========Parser Tests============================#
    #test to see if the system can retrieve header files
    def test_getFilesHeader(self):
        headers,source = getFiles("testsrc")
        self.assertGreater(len(headers),0)

    #test to see if the system can retrieve cpp files
    def test_getFilesSource(self):
        headers,source = getFiles("testsrc")
        self.assertGreater(len(source),0)

    #test to see if one can strip comments
    def test_getFilesCanParseComments(self):
        headers,source = getFiles("testsrc" + os.sep + "parseTest")
        check = False;
        for x in source:
            tempLocation = analyzeGlobalVariables(source[x])
            print(tempLocation)
            if(len(tempLocation) == 0):
                check = True;

        self.assertEqual(check,True)



    #==========Test section for Friends=================#
    #test to see if we can find friends
    def test_AnalyzeFriend(self):
        testFilePath = "testsrc" + os.sep + 'FriendTest' #os.path.dirname(__file__) + os.sep + 
        headers,source = getFiles(testFilePath)
        check = False;
        for x in headers:
            tempLocation = analyzeFriend(headers[x])
            print(tempLocation)
            if(len(tempLocation) > 0):
                check = True;

        self.assertEqual(check,True)

    #test to see if the word friend does not mess with the test
    def test_FalsePostiveFriend(self):
        testFilePath = "testsrc" + os.sep + 'FriendTest' #os.path.dirname(__file__) + os.sep + 
        headers,source = getFiles(testFilePath)
        check = False;
        for x in headers:
            tempLocation = analyzeFriend(headers[x])
            print(tempLocation)
            if(len(tempLocation) > 2):
                check = True;

        self.assertEqual(check,False)

    def test_CanFindMultipleFriends(self):
        testFilePath = "testsrc" + os.sep + 'FriendTest' #os.path.dirname(__file__) + os.sep + 
        headers,source = getFiles(testFilePath)
        check = False;
        for x in headers:
            tempLocation = analyzeFriend(headers[x])
            print(tempLocation)
            if(len(tempLocation) > 1):
                check = True;

        self.assertEqual(check,True)


    #========================Test for global variables

    #test to see if global variables can be found
    def test_findGlobal(self):
        testFilePath = "testsrc" + os.sep + 'GlobalTest' #os.path.dirname(__file__) + os.sep + 
        headers,source = getFiles(testFilePath)
        check = False;
        for x in source:
            tempLocation = analyzeGlobalVariables(source[x])
            print(tempLocation)
            if(len(tempLocation) > 0):
                check = True;
            
        for x in headers:
            tempLocation = analyzeGlobalVariables(headers[x])
            print(tempLocation)
            if(len(tempLocation) > 0):
                check = True;
        self.assertEqual(check,True)

    #checks for scoped variable false postives
    def test_noScopedVariables(self):
        testFilePath = "testsrc" + os.sep + 'GlobalTest' #os.path.dirname(__file__) + os.sep + 
        headers,source = getFiles(testFilePath)
        check = False;
        for x in source:
            tempLocation = analyzeGlobalVariables(source[x])
            print(tempLocation)
            if(len(tempLocation) < 2 and len(tempLocation) > 0):
                check = True;
            
        for x in headers:
            tempLocation = analyzeGlobalVariables(headers[x])
            print(tempLocation)
            if(len(tempLocation) < 2 and len(tempLocation) > 0):
                check = True;
        self.assertEqual(check,True)


    #=============Section for public data members=============#
    #test to check to see if one can find cpp and h headers
    def test_PublicdataMembers(self):
        testFilePath = "testsrc" + os.sep + 'PublicTest' #os.path.dirname(__file__) + os.sep + 
        headers,source = getFiles(testFilePath)
        checkOne = False;
        checkTwo = False;

        for x in source:
            tempLocation = analyzePublicMembers(source[x])
            print(tempLocation)
            if( len(tempLocation) > 0):
                checkOne = True;
         
        for x in headers:
            tempLocation = analyzePublicMembers(headers[x])
            if(len(tempLocation) > 1):
                checkTwo = True;

      

        self.assertEqual(checkOne,True)
        self.assertEqual(checkTwo,True)

    #test to see if private data members are not caught up
    def test_privateDataMembersFine(self):
        testFilePath = "testsrc" + os.sep + 'PublicTest' #os.path.dirname(__file__) + os.sep + 
        headers,source = getFiles(testFilePath)
        checkTwo = False;

        for x in headers:
            tempLocation = analyzePublicMembers(headers[x])
            if(len(tempLocation) > 1 and len(tempLocation) < 3):
                checkTwo = True;

        self.assertEqual(checkTwo,True)

    #checks to see if function is all okay () should not be considered a public data member
    def test_publicFunctionsAreOkay(self):
        testFilePath = "testsrc" + os.sep + 'PublicTest' #os.path.dirname(__file__) + os.sep + 
        headers,source = getFiles(testFilePath)
        checkTwo = False;

        for x in headers:
            tempLocation = analyzePublicMembers(headers[x])
            if(len(tempLocation) > 1 and len(tempLocation) < 3):
                checkTwo = True;

        self.assertEqual(checkTwo,True)

    #==================================Switch Tool Section========================#
    def test_publicFunctionsAreOkay(self):
        testFilePath = "testsrc" + os.sep + 'SwitchTest' #os.path.dirname(__file__) + os.sep + 
        headers,source = getFiles(testFilePath)
        checkTwo = False;
        for x in source:
            tempLocation = analyzeSwitch(source[x])
            if(len(tempLocation) > 0):
                checkTwo = True;

        self.assertEqual(checkTwo,True)
    #This test is to see if swith is used, that is wont be mistaken in a variable
    def test_switchKeyWord(self):
        testFilePath = "testsrc" + os.sep + 'SwitchTest' #os.path.dirname(__file__) + os.sep + 
        headers,source = getFiles(testFilePath)
        checkTwo = False;

        for x in source:
            tempLocation = analyzeSwitch(source[x])
            if(len(tempLocation) > 0 and len(tempLocation) < 2):
                checkTwo = True;

        self.assertEqual(checkTwo,True)

#==============================IMPLEMENTATION TESTING SECTION============================================

#def test_canFindImplementationInheader():
 #   testFilePath = "testsrc" + os.sep + 'inheritanceTest' #os.path.dirname(__file__) + os.sep + 
 #   headers,source = getFiles(testFilePath)
#  totalCount = []
#   for x  in headers:
#       impLine = analyzeImplementationInheritance(headers[x],source,headers)
#       for y in impLine:
#           totalCount.append(y)
#
#    impLine = list(set(totalCount))
       





    

            

if __name__ == '__main__':
    unittest.main()
