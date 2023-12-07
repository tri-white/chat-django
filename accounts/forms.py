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

        self.fields['username'].label = 'Псевдонім'
        self.fields['password'].label = 'Пароль'

    class Meta:
        error_messages = {
            'invalid_login': 'Неправильний псевдонім або пароль. Будь ласка, спробуйте знову.',
            'inactive': 'Цей обліковий запис неактивний.',
            'all': 'Неправильний псевдонім або пароль. Будь ласка, перевірте правильність псевдоніма та паролю.',
        }

from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        error_messages = {
            'username': {
                'unique': 'Це ім\'я користувача вже зайняте. Будь ласка, виберіть інше.',
            },
            'email': {
                'unique': 'Користувач з цією електронною поштою вже існує.',
            },
            'password2': {
                'password_mismatch': 'Введені паролі не збігаються. Будь ласка, введіть однакові паролі.',
            },
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].label = 'Ім\'я користувача'
        self.fields['email'].label = 'Електронна пошта'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Підтвердження паролю'

class UserProfileForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['password']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].help_text = None
        self.fields['password'].label = 'Пароль'


