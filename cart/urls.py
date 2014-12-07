from django.conf.urls import *

urlpatterns = patterns('cart.views',
                       url(r'^$', 'show_cart_new', { 'template_name': 'cart/cart.html' }, 'show_cart'),
)
