# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['avatar', 'password']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].help_text = None

