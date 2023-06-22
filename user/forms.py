from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from django.contrib.auth import get_user_model


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email or Username')


class RegisterForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password']
