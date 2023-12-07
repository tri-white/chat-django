# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)

        # Change labels for fields to Ukrainian
        self.fields['username'].label = 'Псевдонім'
        self.fields['password'].label = 'Пароль'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        # Change labels for fields to Ukrainian
        self.fields['username'].label = 'Ім\'я користувача'
        self.fields['email'].label = 'Електронна пошта'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Підтвердження паролю'

class UserProfileForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['avatar', 'password']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].help_text = None

        # Change labels for fields to Ukrainian
        self.fields['avatar'].label = 'Аватар'
        self.fields['password'].label = 'Пароль'


