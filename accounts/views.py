# -*-coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, HttpResponse,resolve_url
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from  django.contrib.auth.views import login
from accounts import profile

from checkout.models import Order, OrderItem
from accounts.forms import UserProfileForm, RegistrationForm
from django.views.decorators.csrf import csrf_protect

from accounts import profile
from forms import MyAuthenticationForm
from random import choice
from string import letters
from models import UserProfile
import json


def register(request, template_name="registration/register.html"):
    """ view displaying customer registration form """
    """data = request.POST.copy()
    data['username'] = ''.join([choice(letters) for i in xrange(30)])
    request.session.set_test_cookie()
    form = MyAuthenticationForm(request, data=data)"""
    if request.method == 'POST':
        postdata = request.POST.copy()
        postdata['username'] = ''.join([choice(letters) for i in xrange(30)])
        form = RegistrationForm(postdata)
        if form.is_valid():
            #form.save()
            user = form.save(commit=False)  # new
            user.email = postdata.get('email','')  # new
            user.save()  # new
            un = postdata.get('username','')
            pw = postdata.get('password1','')
            from django.contrib.auth import login, authenticate
            new_user = authenticate(username=un, password=pw)
            if new_user and new_user.is_active:
                login(request, new_user)
                url = urlresolvers.reverse('my_account')
                return HttpResponseRedirect(url)
    else:
        form = RegistrationForm()
    page_title = 'Регистрация пользователя'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@csrf_protect
def register_ajax(request):
    """ ajax - регистрация пользователей """
    print("here1")
    response_dict = {}  # ответ клиенту
    if request.method == 'POST':
        postdata = request.POST.copy()
        postdata['username'] = ''.join([choice(letters) for i in xrange(30)])
        form = RegistrationForm(data=postdata)
        if form.is_valid():
            form.save()
            pw = postdata.get('password1', '')
            email = postdata.get('email')
            from django.contrib.auth import login, authenticate
            new_user = authenticate(username=email, password=pw)
            if new_user and new_user.is_active:  # авторизуем зарегестрированного пользователя
                login(request, new_user)
                response_dict.update({'success': 'True'})
        else:
            data = []
            for k, v in form._errors.iteritems():  # формируем словарь ошибок по шаблону  'имя формы' : 'описание ошибки'
                text = {'desc': ', '.join(v),}
                text['key'] = '%s' % k
                data.append(text)
            response_dict.update({'success': 'False','errors': data})
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')

#@login_required
def my_account(request, template_name="registration/my_account.html"):
    """ page displaying customer account information, past order list and account options """
    if request.user.is_authenticated():
        orders = Order.objects.filter(user=request.user)
        orders_item = {}
        for order in orders:
            orders_item.update({order : OrderItem.objects.filter(order=order)})
        print(orders_item)
        userprofile = profile.retrieve(request)
        name = userprofile.name
        #u = get_object_or_404(UserProfile, id = userprofile.id)
        #products = u.favorites_set.all()
        #print(u.favorites_set.all())
        print("ee")
        products = userprofile.favorites.all()
        #print(name)
    page_title = 'Мой аккаунт'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
def order_details(request, order_id, template_name="registration/order_details.html"):
    """ displays the details of a past customer order; order details can only be loaded by the same 
    user to whom the order instance belongs.
    
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    page_title = 'Order Details for Order #' + order_id
    order_items = OrderItem.objects.filter(order=order)
    for i in order_items:
        print(i.total)
        print (i.name)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
def order_info(request, template_name="registration/order_info.html"):
    """ page containing a form that allows a customer to edit their billing and shipping information that
    will be displayed in the order form next time they are logged in and go to check out """
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserProfileForm(postdata)
        if form.is_valid():
            profile.set(request)
            url = urlresolvers.reverse('my_account')
            return HttpResponseRedirect(url)
    else:
        user_profile = profile.retrieve(request)
        form = UserProfileForm(instance=user_profile)
    page_title = 'Edit Order Information'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@csrf_protect
def login(request):
    """ ajax - авторизация пользователей """
    if request.method == "POST":
        form = MyAuthenticationForm(request, data=request.POST)
        response_dict = {}
        if form.is_valid():
            auth.login(request, form.get_user())  # авторизация
            response_dict.update({'success': 'True'})
        else:
            data = []
            for k, v in form._errors.iteritems():  # формируем словарь ошибок по шаблону  'имя формы' : 'описание ошибки'
                text = {'desc': ', '.join(v),}
                text['key'] = '%s' % k
                data.append(text)
            response_dict.update({'success': 'False','errors': data})
        return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
    url = urlresolvers.reverse('my_account')
    return HttpResponseRedirect(url)


def logout(request, now_page=None):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    auth.logout(request)
    return HttpResponseRedirect(now_page)
