# -*- coding: utf-8 -*-
from cart import cart
from django.core import urlresolvers
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from Store.settings import FROM_EMAIL
from models import SHIPPING_CHOICES

def get_checkout_url(request):
    return urlresolvers.reverse('checkout')


from models import Order

def create_order(request):
    """ if the POST to the payment gateway successfully billed the customer, create a new order
    containing each CartItem instance, save the order with the transaction ID from the gateway,
    and empty the shopping cart

    """
    order = Order()
    #checkout_form = MyCheckoutForm(request.POST, instance=order)
    #order = checkout_form.save(commit=False)

    order.ip_address = request.META.get('REMOTE_ADDR', '') or request.META.get('HTTP_X_FORWARDED_FOR', '')
    order.user = None
    if request.user.is_authenticated():
        order.user = request.user
    order.email = request.POST['email']
    order.phone = request.POST['phone']
    order.name = request.POST['name']
    order.status = Order.SUBMITTED

    order.shipping = request.POST["shipping"]
    #print(SHIPPING_CHOICES[0:1])
    print(SHIPPING_CHOICES[1][0])
    print(order.shipping)
    if (order.shipping == SHIPPING_CHOICES[1][0]):
        print("ok")
        order.address = request.POST["address"]
    print(order.address)
    print(order.shipping)
    print(order)
    order.save()

    if order.pk:
        """ if the order save succeeded """
        cart_items = cart.get_cart_items(request)
        for ci in cart_items:
            print("weight")
            """ create order item for each cart item """
            from models import OrderItem
            oi = OrderItem()
            oi.order = order
            oi.quantity = ci.quantity
            oi.price = ci.price  # now using @property
            if ci.description:
                oi.description = ci.description
            print("weight______1___")
            print(ci.weight)
            oi.weight = ci.weight
            print(oi.weight)
            print(oi.filling)
            oi.filling = ci.filling
            oi.product = ci.product
            oi.save()
            print("oi!!!")
            print(oi)
        # all set, clear the cart

        #send_email(request,order.id)
        cart.empty_cart(request)

        # save profile info for future orders
        if request.user.is_authenticated():
            from accounts import profile
            print ("profile")
            profile.set(request)
    return order


def send_email(request, order_number):
    postdata = request.POST.copy()
    name = postdata["name"]
    to = postdata["email"]

    rend_dic = {}
    rend_dic.update({'cart_items': cart.get_cart_items(request), 'name': name})
    print(rend_dic)
    html = render_to_string("email/send_order.html",rend_dic)

    title = ("Заказ № "+str(order_number))

    msg = EmailMessage(title, html, FROM_EMAIL, [to])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()

def process(request):
    order = create_order(request)
    results = {'order_number': order.id, 'message': u''}
    return results