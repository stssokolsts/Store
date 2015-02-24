# -*- coding: utf-8 -*-
from django import template
import locale

register = template.Library()

@register.filter(name='currency1')
def currency(value):

    locale.setlocale(locale.LC_ALL,'')
    loc = locale.localeconv()
    return locale.currency(value, loc['currency_symbol'], grouping=True)

@register.filter(name='currency')
def currency1(value):
    value = '{:20,.1f}'.format(value)
    s = str((value))
    return (s.split('.')[0]+ (" p"))