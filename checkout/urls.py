from django.conf.urls import *
from Store import settings


urlpatterns = patterns('checkout.views',
    url(r'^$', 'show_checkout', {'template_name': 'checkout/checkout.html'}, 'checkout'),
    url(r'^receipt/$', 'receipt', {'template_name': 'checkout/receipt.html'},'checkout_receipt'),
) 