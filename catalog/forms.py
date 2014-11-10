# -*- coding: utf-8 -*-
from catalog.models import Product
from django import forms
from catalog.models import Filling


class AddToCart(forms.Form):
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'size':'2', 'value':'1', 'class': 'form-control'}),
                                  error_messages={'invalid':'Please enter a valid quantity.'},
                                  label='Количество: ',
                                  min_value=1,
                                  max_value=100)

    def __init__(self, request=None, *args, **kwargs):
        """ override the default so we can set the request """
        self.request = request
        super(AddToCart, self).__init__(*args, **kwargs)

    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Cookies must be enabled.")
        return self.cleaned_data

class AddToCartFromCategory(AddToCart):
    product_slug = forms.CharField(widget=forms.HiddenInput())

class AddToCartForm(forms.Form):
    description = forms.CharField (widget=forms.Textarea(attrs={'class':'form-control', 'rows': '3',
                                        'placeholder': "Любое оформление верхушки торта"}),
                                   label='Выбор оформления: ',
                                   required=False)
    product_slug = forms.CharField(widget=forms.HiddenInput())
    filling_choice = forms.ModelChoiceField(queryset=Filling.active.all(),
                                            empty_label=None,
                                            label="Основа:",
                                            widget=forms.Select(attrs={'class':'form-control'}),
                                            )
    weight = forms.FloatField (widget=forms.TextInput(attrs={'size': '2','value':'1','class':'form-control'}),
                                error_messages={'invalid' : 'Пожалуйста, введите корректное значение!'},
                                min_value=1, max_value=20,
                                label='Вес: ')
    #quantity = forms.IntegerField(widget=forms.TextInput(attrs={'size':'2', 'value':'1', 'class':'quantity'}),
                                 # error_messages={'invalid':'Please enter a valid quantity.'},
                                  #min_value=1)

    def __init__(self, request=None, *args, **kwargs):
        """ override the default so we can set the request """
        self.request = request
        super(AddToCartForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Cookies must be enabled.")
        return self.cleaned_data




class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product

    def clean_price(self):
        if self.cleaned_data['price'] <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return self.cleaned_data['price']
