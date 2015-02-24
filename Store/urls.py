from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

handler404 = 'Store.views.file_not_found_404'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Store.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^checkout/', include('checkout.urls')),
    url(r'^', include('catalog.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^social/', include('social_auth.urls')),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)