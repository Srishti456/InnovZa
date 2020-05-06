from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import request
from tinymce import TinyMCE
from .models import UserInfo,Post,Comment,ProjectComment

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('username','password','email',)

class UserDataForm(forms.ModelForm):
    class Meta:
        model=UserInfo
        fields=('full_name','username','phoneno','gender',)

class CommentForm(forms.ModelForm):
    content=forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'Type Your Comment',
        'id':'usercomment',
        'rows':'2',
    }))
    class Meta:
        model=Comment
        fields=('content',)

class ProjectCommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type Your Comment',
        'id': 'usercomment',
        'rows': '2',
    }))

    class Meta:
        model = ProjectComment
        fields = ('content',)
