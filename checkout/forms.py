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
    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Order
        exclude = ('status', 'ip_address', 'user',)
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter email', 'type':'email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Контактный телефон', 'type':'text'})
        }
        labels = {
            'phone' : ('Телефон'),
        }