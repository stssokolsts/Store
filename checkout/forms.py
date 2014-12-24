# -*- coding: utf-8 -*-
from django import forms
from models import Order
from Store.settings import DEBUG
from django.contrib.auth.models import User
import datetime
from models import SHIPPING_CHOICES
from django.contrib.auth.forms import AuthenticationForm
import re

#CHOICES = (('1', 'Самовывоз',), ('2', 'Доставка',))

def strip_non_numbers(data):
    """ gets rid of all non-number characters """
    non_numbers = re.compile('\D')
    return non_numbers.sub('', data)

class CheckoutForm(forms.ModelForm):
    def __init__(self, email = None, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.fields['name'].help_text = 'Пожалуйста,укажите настоящие имя и фамилию. ' \
                                        'По этому имени мы будем обращаться к Вам для уточнения деталей заказа'
        self.fields['phone'].help_text = 'Ваш телефон необходим для связи с Вами'
        self.fields['email'].help_text = 'На этот e-mail будет выслано письмо с ' \
                                         'информацией о заказе и чек, подтверждающий оплату ' \
                                         '(в случае оплаты через электронную коммерцию)'
        #print(self.fields['shipping'].choices["1"]) #= self.fields['shipping'].choices[1:]
        #print(self.fields["shipping"].data)
        print(SHIPPING_CHOICES[1])
        if (self.fields["shipping"].choices ==SHIPPING_CHOICES[1] ):
            print("ok")
        if email:
            self.fields['email'].widget.attrs['value'] = email


    class Meta:
        model = Order
        exclude = ('status', 'ip_address', 'user',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов Иван', 'type':'text'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '79101234567', 'type':'text'}),
            'email' : forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'useremail@example.com'}),
            'shipping' : forms.RadioSelect(),
            'billing' : forms.RadioSelect(),
            'address': forms.TextInput(attrs={'class' : 'address-form-control',
                                              'placeholder':'Введите адрес доставки в произвольной форме',
                                              'type':'text'})
        }
        labels = {
            'phone': ('Телефон'),
            'name': ('Контактное лицо'),
            'email': ("E-mail"),
            'address': ("Адрес доставки"),
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        print (email)
        return email
        try:
            user = User.objects.get(email=email)
            print(user)
            self._errors["email"] = "На этот почтовый ящик зарегестрирован другой аккаунт. Пожалуйста,проверьте " \
                                    "правильность правильность написания этого поля или войдите,используя этой e-mail"
            raise forms.ValidationError("На этот почтовый ящик зарегестрирован другой аккаунт. Пожалуйста,проверьте "
                                        "правильность правильность написания этого "
                                        "поля или войдите,используя этой e-mail")
        except User.DoesNotExist:
            return email