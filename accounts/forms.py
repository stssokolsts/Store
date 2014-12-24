# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'favorites')


class RegistrationForm(UserCreationForm):
    """ Расширенная форма регистрации пользователей """
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

    password1 = forms.CharField(label="Пароль",
                                 help_text= 'Пароль должен быть длинной не менее 6 символов',
                                 widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '*******'}), min_length=6)
    password2 = forms.CharField(label="Повторите пароль",
                                 widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': '*******'}), min_length=6)
    email = forms.EmailField(label=("E-mail"),max_length="75",
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'useremail@example.com'}),
                             help_text=("Ваш e-mail будет использоваться"
                                        " для подтверждения отправки заказа и уведомления об изменении его статуса"),)

    name = forms.CharField(label=("Имя пользователя"), max_length=150,
        widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов Иван'}),
        help_text=("Пожалуйста, введите настоящее имя и фамилию. "
                   "По этому имени мы будем обращаться к Вам для уточнения деталей заказов"),
        )

    class Meta:
        model = User
        fields = ('name', 'email',)

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            raise forms.ValidationError("На этот e-mail уже зарегистрирован аккаунт")
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
        user_profile.user = user
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