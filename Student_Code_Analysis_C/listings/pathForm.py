from django import forms

class getPath(forms.Form):
    filePath = forms.CharField(required=True)