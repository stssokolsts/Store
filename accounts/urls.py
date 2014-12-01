from django.conf.urls import *
from Store import settings

urlpatterns = patterns('accounts.views',
                       #url(r'^register/$', 'register',
                           #{'template_name': 'registration/register.html'}, 'register'),
                       url(r'^register/$', 'register_ajax',
                           {}, 'register_ajax'),
                       #url(r'^logout/$','logout',{},'logout'),
                       url(r'^my_account/$', 'my_account',
                           {'template_name': 'registration/my_account.html'}, 'my_account'),
                       url(r'^order_info/$', 'order_info',
                           {'template_name': 'registration/order_info.html'}, 'order_info'),
                       url(r'^order_details/(?P<order_id>[-\w]+)/$', 'order_details',
                           {'template_name': 'registration/order_details.html'}, 'order_details'),
                       url(r'login/$', 'login', {}, 'login'),
)

#urlpatterns += patterns('django.contrib.auth.views', (r'^login/$', 'login',
#                                                      {'template_name': 'registration/login.html', }, 'login'),
#)
