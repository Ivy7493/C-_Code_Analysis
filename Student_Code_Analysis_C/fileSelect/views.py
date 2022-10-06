from fileinput import filename
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from listings.pathForm import getPath
from django.urls import reverse
from ProcessController import ProcessController as PrscC
import os
from django.db import models
import json
from ast import literal_eval

class AnalysisInformation(models.Model):
    first_name = models.CharField(
        max_length=100
    )
    last_name = models.CharField(
        max_length=100
    )
    job_title = models.CharField(
        max_length=200
    )

def fileSelectHome(request):
    
    form = getPath()
   
    return render(request,'fileSelect/fileSelectHome.html',{'form':form})


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
    return render(request,'fileSelect/fileDisplay.html',{'title':'File Viewer'})

def displayCode(request):
    fileRaw = request.POST["val"]
    file = literal_eval(fileRaw)
    
    for x in file:
        print(x)
    
    return render(request,'fileSelect/displayCode.html',{'file':file})