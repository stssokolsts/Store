# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response,HttpResponse,urlresolvers,HttpResponseRedirect
from django.template import RequestContext
from catalog.models import Product
from cart import cart
import search,socket,json

def results(request, template_name="search/result.html"):
    q = request.GET.get('q', '')
    page_title = "Результаты поиска по запросу '"+q.encode('utf-8')+"'"
    s = socket.socket()
    address = '127.0.0.1'
    port = 9312 # port number is a number, not string
    try:
        s.connect((address, port))
        products = Product.search.query(q)
        print("sphinx")
        print(q)
        print(products)
    except Exception, e:
        print('something\'s wrong with %s:%d. Exception type is %s' % (address, port, `e`))
        products = search.products_def(q).get('products', [])
    #print(list(products))
    detail = True

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
# Create your views here.
