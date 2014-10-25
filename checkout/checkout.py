from cart import cart
from models import OrderItem
from Store import settings
from django.core import urlresolvers
import urllib


def get_checkout_url(request):
    return urlresolvers.reverse('checkout')


from models import Order

def my_create_order(request):
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
    order.status =Order.SUBMITTED
    order.save()

    if order.pk:
        """ if the order save succeeded """
        cart_items = cart.get_cart_items(request)
        for ci in cart_items:
            """ create order item for each cart item """
            from models import MyOrderItem
            oi = MyOrderItem()
            oi.order = order
            oi.quantity = ci.quantity
            oi.price = ci.price  # now using @property
            oi.product = ci.product
            oi.save()
        # all set, clear the cart
        cart.empty_cart(request)

        # save profile info for future orders
        if request.user.is_authenticated():
            from account import profile
            profile.set(request)
    return order

def my_process(request):
    order = my_create_order(request)
    results = {'order_number': order.id, 'message': u''}
    return results