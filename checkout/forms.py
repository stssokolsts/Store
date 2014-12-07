# -*- coding: utf-8 -*-
from django import forms
from models import Order
from Store.settings import DEBUG
import datetime
import re

def strip_non_numbers(data):
    """ gets rid of all non-number characters """
    non_numbers = re.compile('\D')
    return non_numbers.sub('', data)

class CheckoutForm(forms.ModelForm):
    def __init__(self, email = None, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.fields['name'].help_text = 'Пожалуйста,укажите настоящие имя и фамилию'
        self.fields['phone'].help_text = 'Например, 79101234567'
        if email:
            self.fields['email'].widget.attrs['value'] = email

    class Meta:
        model = Order
        exclude = ('status', 'ip_address', 'user',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов Иван Иванович', 'type':'text'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Контактный телефон', 'type':'text'}),
            'email' : forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'useremail@example.com'})
        }
        labels = {
            'phone' : ('Телефон'),
            'name' : ('Контактное лицо'),
            'email': ("E-mail")
        }