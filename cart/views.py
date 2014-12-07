#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, urlresolvers, HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from checkout import checkout
from catalog.forms import AddToCart
from accounts import profile
from checkout.forms import CheckoutForm
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
    request.session.set_test_cookie()
    #заполняем форму если пользователь авторизован
    if request.user.is_authenticated():
        user_profile = profile.retrieve(request)
        email = user_profile.user.email
        form_checkout = CheckoutForm(instance=user_profile, email = email )
    else:
        form_checkout = CheckoutForm()

    if request.method == 'POST':
        print("метод пост")
        postdata = request.POST.copy()
        print(postdata)
        form_q = AddToCart(request, data=postdata)
        if postdata['submit'] == 'Remove':
            print("удалить")
            if request.is_ajax():
                #удаление ajax'ом
                success = cart.remove_from_cart(request, ajax=True)
                response_dict = {}
                response_dict.update({'count': cart.get_cart_items(request).count(),
                                      'cart_subtotal': cart.cart_subtotal(request)})
                if success==True:
                    response_dict.update({'success': 'True'})
                else:
                     response_dict.update({'success': 'False'})
                return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
            #обычное удаление
            cart.remove_from_cart(request)
        if postdata['submit'] == 'Update':
            print("обновить")
            quantity = postdata['quantity']
            form_q.fields['quantity'].widget.attrs['value'] = quantity
            print(form_q.errors.as_ul)
            if form_q.is_valid():
                print("форма обновления валидна")
                cart.update_cart(request)
            else:
                print("форма обновления не валидна")
                error_message = u'Correct the errors below'
        #пытаемся отправить заказ
        if postdata['submit'] == 'Checkout':
            print("отправить")
            form_checkout = CheckoutForm(data=postdata)
            if form_checkout.is_valid():
                print("форма информации валидна")
                #отправляем
                response = checkout.process(request)
                order_number = response.get('order_number', 0)
                error_message = response.get('message', '')
                if order_number:
                    #задем номер заказа в сессии
                    print("номер получен")
                    request.session['order_number'] = order_number
                    receipt_url = urlresolvers.reverse('checkout_receipt')
                    return HttpResponseRedirect(receipt_url)
            else:
                print("форма информации не валидна")
                print (form_checkout.errors.as_ul)
                error_message = u'Correct the errors below'
    cart_items = cart.get_cart_items(request)
    page_title = 'Корзина'
    cart_subtotal = cart.cart_subtotal(request)
    return render_to_response(template_name, locals(),context_instance=RequestContext(request))
# Create your views here.