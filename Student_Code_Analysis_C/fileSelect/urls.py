from django.urls import path
from . import views

urlpatterns = [
    path('', views.fileSelectHome,name = "studentAnalysisHome"),
    path('fileDisplay/',views.executeProgram,name = "fileDisplay"),
    path('executeProgram/',views.executeProgram,name ="executeProgram"),
    path('navBarLaunch/',views.navBarLaunch, name="navBarLaunch"),
    path('executeProgram/displayCode/',views.displayCode,name = "displayCode"),
]