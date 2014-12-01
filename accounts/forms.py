# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)


class RegistrationForm(UserCreationForm):
    """ Расширенная фФорма регистрации пользователей """
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

    password1 = forms.RegexField(label="Пароль", regex=r'^(?=.*\W+).*$',
                                 help_text= 'Пароль должен быть длинной не менее 6 символов и содержать хотя бы один не алфавитно-цифровой символ.',
                                 widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '*******'}), min_length=6)
    password2 = forms.RegexField(label="Повторите пароль", regex=r'^(?=.*\W+).*$',
                                 widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': '*******'}), min_length=6)
    email = forms.EmailField(max_length="75", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'useremail@example.com'}))

    name = forms.CharField(label=("Имя пользователя"), max_length=150,
        widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов Иван Иванович'}),
        help_text=("По этому имени мы будем обращаться к Вам для уточнения деталей"),
        )

    class Meta:
        model = User
        fields = ('name', 'email',)

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            raise forms.ValidationError("This email address already exists. Did you forget your password?")
        except User.DoesNotExist:
            return email

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["username"]
        user.is_active = True # change to false if using email activation
        if commit:
            user.save()
        user_profile = UserProfile()
        user_profile.name = self.cleaned_data["name"]
        user_profile.user.id = user.id
        user_profile.name = self.cleaned_data["name"]
        user_profile.save()
        return user


class MyAuthenticationForm(AuthenticationForm):
    """форма авторизации с использованием email  в качестве логина"""
    def __init__(self, request = None, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(request, *args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = 'E-mail'
        self.fields['password'].label = 'Пароль'

    error_messages = {
        'invalid_login': ("Пожалуйста, проверьте правильность написания e-mail и пароля."
            " Заметьте,оба поля регистрочувствительны"),
        'inactive': ("К сожалению, этот аккаунт был заблокирован"),
    }