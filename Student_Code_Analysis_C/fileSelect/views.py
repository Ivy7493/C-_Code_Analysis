from fileinput import filename
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from listings.pathForm import getPath
from django.urls import reverse
from ProcessController import ProcessController as PrscC
import os
from ast import literal_eval
from persistentService import saveData,getData

def fileSelectHome(request):
    
    form = getPath()
   
    return render(request,'fileSelect/fileSelectHome.html',{'form':form})


def executeProgram(request):
    folder = request.POST["filePath"]
    headers,sources,occurArr = PrscC(os.path.join(folder))
    saveData('issues',occurArr)
    context = {
        'title':'File Viewer',
        'headers':headers,
        'sources':sources,
    }
    
    return render(request,'fileSelect/fileDisplay.html',context)

def viewReport(request):
    return render(request,'fileSelect/fileDisplay.html',{'title':'File Viewer'})

def displayCode(request):
    fileRaw = request.POST["val"]
    file = literal_eval(fileRaw)
    issues = getData("issues")[0]
    for x in issues:
        print(x)
    return render(request,'fileSelect/displayCode.html',{'file':file})