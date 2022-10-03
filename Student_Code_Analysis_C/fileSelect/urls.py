from django.urls import path
from . import views

urlpatterns = [
    path('', views.fileSelectHome,name = "studentAnalysisHome"),
    path('viewReport/',views.viewReport,name = "viewReport"),
    path('executeProgram/',views.executeProgram,name ="executeProgram")
]