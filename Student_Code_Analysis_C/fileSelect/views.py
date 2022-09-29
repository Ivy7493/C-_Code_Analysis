from django.shortcuts import render
from django.http import HttpResponse


posts = [
    {
        'filelocation':r"C:\Users\fouri\Documents\aUniversity\Electrical Engineering\3rd Year\2nd Semester\ELEN3009\Course Project\Course project\src",
        'other':'other'
    },
    {
        'filelocation':r'C:\Users\fouri\Documents\aUniversity\Electrical Engineering\4th Year\1st semester\ELEN4002\Project\Student Projectss\Musa project C++\project-repo\src\game-source-code',
        'other':'other'
    }
]

def fileSelectHome(request):
    context = {
        'files':posts
    }
    return render(request,'fileSelect/fileSelectHome.html')
def fileReader(request):
    return render(request,'fileSelect/fileDisplay.html')