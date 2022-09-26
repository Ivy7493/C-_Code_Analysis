import unittest
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

    def testAnalyzeFriend(self):
        testFilePath = "testsrc" #os.path.dirname(__file__) + os.sep + 
        headers,source = getFiles(testFilePath)
        check = False;
        for x in headers:
            temp,tempLocation = analyzeFriend(headers[x])
            print(tempLocation)
            if(len(tempLocation) > 0):
                check = True;

        self.assertEqual(check,True)    
            

if __name__ == '__main__':
    unittest.main()
