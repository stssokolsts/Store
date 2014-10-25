from django.conf.urls import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = patterns('catalog.views',
                       url(r'^$', 'index', { 'template_name' :'catalog/index.html'}, 'catalog_home'),
                       url(r'^category/(?P<category_slug>[-\w]+)/$', 'show_category', {'template_name':'catalog/category.html'},
                           'catalog_category'),
                       url(r'^product/(?P<product_slug>[-\w]+)/$', 'show_product', {'template_name':'catalog/product.html'},
                           'catalog_product'),
                       url(r'^catalog$','show_catalog',{'template_name':'catalog/catalog.html' },'catalog'),
                       url(r'^akcii/', 'show_discounts', {'template_name':'catalog/discounts.html'},
                           'discounts'),
                       url(r'^product/add/$', 'add_product_cart'),
                       )

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)