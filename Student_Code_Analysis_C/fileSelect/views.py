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
<<<<<<< HEAD
    print("WHORE !")
=======
    print("WHORE")
>>>>>>> b07b63d... Redirects correctly to a new page
    context = {
        'title':'File Viewer',
        'headers':headers,
        'sources':sources,
        'countArr':countArr,
        'occurArr':occurArr,
    }
<<<<<<< HEAD
    print("WHORE2")
=======
>>>>>>> b07b63d... Redirects correctly to a new page
    return render(request,'fileSelect/fileDisplay.html',context)

def viewReport(request):
    print("here")
    return render(request,'fileSelect/fileDisplay.html',{'title':'File Viewer'})
