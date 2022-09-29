from django.urls import path
from . import views

urlpatterns = [
    path('', views.fileSelectHome,name = "studentAnalysisHome"),
    path('fileReader/',views.fileReader,name = "fileReaderStudentCode")
]