from django import forms
from .models import FaceSignIn

class SignUpForm(forms.ModelForm):
    class Meta:
        model = FaceSignIn
        fields = ['username']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)

