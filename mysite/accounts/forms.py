from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=45)
    password = forms.CharField(required=True, max_length=30, widget=forms.PasswordInput)

