from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email or Username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Email or username',
            'id': 'username-login'  # Set a custom id for the username field
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Password',
            'id': 'password-login'  # Set a custom id for the password field
        })


class RegisterForm(forms.ModelForm):
    password_rep = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(
        attrs={'placeholder': 'Repeat Password', 'id': 'password_rep'}))

    # register_submit = forms.CharField(label='Repeat Password', )

    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password',
                  'password_rep']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
        }
