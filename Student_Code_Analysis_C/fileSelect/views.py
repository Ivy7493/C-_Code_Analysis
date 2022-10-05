from fileinput import filename
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from listings.pathForm import getPath
from django.urls import reverse
from ProcessController import ProcessController as PrscC
import os


fileLocations = [
    {
        'filelocation':'src',
        'other':'other1'
    },
    {
        'filelocation':'gameSourcecode',
        'other':'other2'
    }
]

def fileSelectHome(request):
    
    form = getPath()
    context = {
        'fileLocations':fileLocations,
        'form':form
    }
   
    return render(request,'fileSelect/fileSelectHome.html',context)


def executeProgram(request):
    folder = request.POST["filePath"]
    headers,sources,countArr,occurArr = PrscC(os.path.join(folder))
    print("WHORE !")
    context = {
        'title':'File Viewer',
        'headers':headers,
        'sources':sources,
        'countArr':countArr,
        'occurArr':occurArr,
    }
    return render(request,'fileSelect/fileDisplay.html',context)

def viewReport(request):
    print("here")
    return render(request,'fileSelect/fileDisplay.html',{'title':'File Viewer'})

def displayCode(request):
    fileRaw = request.POST["val"]
    # if ".h" in fileName:
    #     fileList = request.POST.get("headers")
    # elif ".cpp" in fileName:
    #     fileList = request.POST.get("sources")
    # headers,sources,countArr,occurArr = PrscC(os.path.join(folder))
    # context = {
    #     'headers':headers,
    #     'sources':sources,
    #     'countArr':countArr,
    #     'occurArr':occurArr,
    # }        
    # for x in fileList:
    #     print(" ")
    #     print("Item: ", x)
    #     for y in fileList[x]:
    #         print(y)
            
    # context = {
    #     'fileList':fileList,
    #     'fileName':fileName,
    # }
    file = fileRaw.split(',')
    for line in file:
        print(line) 
        
    return render(request,'fileSelect/displayCode.html',{'file':file})
