from django import forms
from .models import UploadedFile

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']  #  The form will handle the 'file' field
        widgets = {
            'file': forms.FileInput(attrs={'multiple': True}), #enables multiple file uploads
        }