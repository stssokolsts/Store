# -*- coding: utf-8 -*-
from django.core import urlresolvers
from django.shortcuts import get_object_or_404, render_to_response
from catalog.models import Category, Product, Filling
from catalog.forms import AddToCartForm, AddToCartFromCategory
from django.template import RequestContext
from cart import cart
from django.http import HttpResponseRedirect, HttpResponse
import json
import operator
from django.core.cache import cache
from Store.settings import CACHE_TIMEOUT
from django.db.models import Q
from sessions import set_last_product
#from stats import stats
#from EcomStore.settings import PRODUCTS_PER_ROW


def index(request, template_name="catalog/index.html"):
    page_title = 'Вкусный праздник - '
    meta_keywords = ''
    meta_description = ''
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def show_category(request, category_slug, template_name="catalog/category.html"):
    category_cache_key = request.path
    c = cache.get(category_cache_key)
    if not c:
        c = get_object_or_404(Category.active, slug=category_slug)
        cache.set(category_cache_key, c, CACHE_TIMEOUT)
    request.session.set_test_cookie()
    c = get_object_or_404(Category, slug=category_slug)
    products = c.product_set.all()
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    #добавляем в корзину
    if request.method == 'POST':
        cart.add_to_cart(request,request.POST.copy())
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            if request.is_ajax():
                response_dict = {}
                response_dict.update({'success': 'True', 'count' : cart.cart_distinct_item_count(request) })
                return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
            url = urlresolvers.reverse('show_cart')
            return HttpResponseRedirect(url)
    request.session.set_test_cookie()
    #костыли для сортировки
    id_sort = request.GET.get('category_id')
    if (id_sort == "namea"):
        products = c.product_set.order_by('name')
        return render_to_response("tags/product_thumbnail.html", locals(), context_instance=RequestContext(request))
    elif (id_sort=="named"):
        products = c.product_set.order_by('-name')
        return render_to_response("tags/product_thumbnail.html", locals(), context_instance=RequestContext(request))
    elif (id_sort=="pricea"):
        products = c.product_set.order_by('price')
        return render_to_response("tags/product_thumbnail.html", locals(), context_instance=RequestContext(request))
    elif (id_sort=="priced"):
        products = c.product_set.order_by('-price')
        return render_to_response("tags/product_thumbnail.html", locals(), context_instance=RequestContext(request))
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def show_discounts(request, template_name="catalog/discounts.html"):
    products = Product.active.filter(old_price__gt=0)
    page_title = "Акции и скидки"
    meta_keywords = ''
    meta_description = ''
    if request.method == 'POST':
        cart.add_to_cart(request, request.POST.copy())
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            if request.is_ajax():
                response_dict = {}
                response_dict.update({'success': 'True', 'count' : cart.cart_distinct_item_count(request) })
                return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
        url = urlresolvers.reverse('show_cart')
        return HttpResponseRedirect(url)
    request.session.set_test_cookie()
    #meta_keywords = c.meta_keywords
    return render_to_response(template_name, locals(), context_instance = RequestContext(request))


def show_catalog(request,template_name="catalog/catalog.html"):
    page_title = 'Каталог'
    categories = Category.active.all()
    meta_keywords = ''
    meta_description = ''
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def show_product(request, product_slug, template_name="catalog/product.html"):
    product_cache_key = request.path
    p = cache.get(product_cache_key)
    if not p:
        p = get_object_or_404(Product.active, slug=product_slug)
        cache.set(product_cache_key, p, CACHE_TIMEOUT)
    p = get_object_or_404(Product, slug=product_slug)
    set_last_product(request,p.slug)
    print(request.session["last_products"])
    categories = p.categories.all()
    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description
    fillings = Filling.active.all()
    m = meta_keywords.split(" ")
    m = filter(None,m)
    print("ага")
    other_products = Product.object.filter(reduce(operator.or_, (Q(meta_keywords__icontains = word) for word in m)))
    print(other_products)
    other_products = other_products.exclude(slug__exact = product_slug)[:4]
    print(other_products)
    postdata = request.POST.copy()
    if request.method == 'POST':
        if (p.choice_weight):
            form_cart = AddToCartForm(request,postdata)
        else:
            form_cart = AddToCartFromCategory(request,postdata)
        httpresp = cart.add_to_cart_general(form_cart,request,p)
        if ( httpresp.get('redirect')):
            return httpresp.get('http_response')
    else:
        if (p.choice_weight):
            form_cart = AddToCartForm(request=request)
        else:
            form_cart = AddToCartFromCategory(request=request)
    form_cart.fields['product_slug'].widget.attrs['value'] = product_slug
    request.session.set_test_cookie()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))