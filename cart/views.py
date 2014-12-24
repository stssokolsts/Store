#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, urlresolvers, HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from checkout import checkout
from catalog.forms import AddToCart
from accounts import profile
from checkout.forms import CheckoutForm
from django.core.mail import send_mail

import cart
import json

def show_cart(request, template_name="cart/cart.html"):
    """ view function for the page displaying the customer shopping cart, and allows for the updating of quantities
    and removal product instances
    """
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = AddToCart(request, postdata)
        if postdata['submit'] == 'Remove':
            cart.remove_from_cart(request)
        if postdata['submit'] == 'Update':
            quantity = postdata['quantity']
            form.fields['quantity'].widget.attrs['value'] = quantity
            print(form.errors.as_ul)
            if form.is_valid():
                print("oooooooooooooooooook!")
                cart.update_cart(request)
            else:
                print("errors")
        if postdata['submit'] == 'Checkout':
            checkout_url = checkout.get_checkout_url(request)
            return HttpResponseRedirect(checkout_url)
    else:
        if request.user.is_authenticated():
            user_profile = profile.retrieve(request)
            form = CheckoutForm(instance=user_profile)
        else:
            form = CheckoutForm()
    cart_items = cart.get_cart_items(request)
    page_title = 'Shopping Cart'
    cart_subtotal = cart.cart_subtotal(request)
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))


def show_cart_new(request, template_name="cart/cart.html"):
    """страница корзины и отправки заказа"""

    cart_items = cart.get_cart_items(request)
    c = cart_items
    print(cart_items)
    request.session.set_test_cookie()
    #заполняем форму если пользователь авторизован
    if request.user.is_authenticated():
        user_profile = profile.retrieve(request)
        email = user_profile.user.email
        form_checkout = CheckoutForm(instance=user_profile, email = email )
    else:
        form_checkout = CheckoutForm()
    if request.method == 'POST':
        postdata = request.POST.copy()
        form_q = AddToCart(request, data=postdata)
        if postdata['submit'] == 'Remove':
            if request.is_ajax():
                #удаление ajax'ом
                return HttpResponse(json.dumps(cart.remove_from_cart_ajax(request)), content_type='application/javascript')
            #обычное удаление
            cart.remove_from_cart(request)
        if postdata['submit'] == 'Update':
            if request.is_ajax():
                return HttpResponse(json.dumps(cart.update_cart_ajax(request)), content_type='application/javascript')
            quantity = postdata['quantity']
            form_q.fields['quantity'].widget.attrs['value'] = quantity
            if form_q.is_valid():
                cart.update_cart(request)
            else:
                print("форма обновления не валидна")
                error_message = u'Введено некоректное значение!'
        #пытаемся отправить заказ
        if postdata['submit'] == 'Checkout':
            print("ch")
            if cart.is_empty(request):
                cart_url = urlresolvers.reverse('show_cart')
                return HttpResponseRedirect(cart_url)
            form_checkout = CheckoutForm(data=postdata)
            print(postdata)
            if form_checkout.is_valid():
                #отправляем
                response = checkout.process(request)
                order_number = response.get('order_number', 0)
                error_message = response.get('message', '')
                if order_number:
                    receipt_url = urlresolvers.reverse('checkout_receipt')
                    return HttpResponseRedirect(receipt_url)
    #cart_items = cart.get_cart_items(request)
    page_title = 'Корзина'
    cart_subtotal = cart.cart_subtotal(request)
    print(form_checkout)
    from checkout.models import SHIPPING_CHOICES
    print(SHIPPING_CHOICES[0][1])
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))
# Create your views here.