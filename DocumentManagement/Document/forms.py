from django import forms
from .models import FileUpload, FileShare
from django.contrib.auth.models import User


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('title', 'file', 'description')
        widgets = {
            'file': forms.FileInput(attrs={'accept': '.png,.jpg,.pdf,.docx'})
        }


class UserShareForm (forms.ModelForm):
    class Meta:
        model = FileShare
        fields = ['share_with']

