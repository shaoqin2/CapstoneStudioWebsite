from django import forms
from django.contrib.auth import authenticate


class loginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password', max_length=50)
