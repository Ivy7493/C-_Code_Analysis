from django.shortcuts import render
from django.http import HttpResponse
from listings.pathForm import getPath


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
def fileReader(request):
    return render(request,'fileSelect/fileDisplay.html',{'title':'File Viewer'})