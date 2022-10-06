from fileinput import filename
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from listings.pathForm import getPath
from django.urls import reverse
from ProcessController import ProcessController as PrscC
import os
import json
from ast import literal_eval

def fileSelectHome(request):
    
    form = getPath()
   
    return render(request,'fileSelect/fileSelectHome.html',{'form':form})


def executeProgram(request):
    folder = request.POST["filePath"]
    headers,sources,countArr,occurArr = PrscC(os.path.join(folder))
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
    
    return render(request,'fileSelect/displayCode.html',{'file':file})