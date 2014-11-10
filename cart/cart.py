# -*- coding: utf-8 -*-
from models import CartItem
from catalog.models import Product
from django.shortcuts import get_object_or_404 
from django.http import HttpResponseRedirect

import decimal# not needed yet but we will later
import random
CART_ID_SESSION_KEY = 'cart_id'

# get the current user's cart id, sets new one if blank
def _cart_id(request):
    if request.session.get(CART_ID_SESSION_KEY, '') == '':
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]


def _generate_cart_id():
    """генерируем уникальный id карты"""
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters)-1)]
    return cart_id


def get_cart_items(request):
    """Возвращает все продкты из текущей карты пользователя"""
    return CartItem.objects.filter(cart_id=_cart_id(request))


def add_to_cart(request, postdata):
    """Добавляем в карту"""
    product_slug = postdata.get('product_slug', '')
    quantity = postdata.get('quantity', 1)
    description = postdata.get('description', '')

    fillings = postdata.get('filling_choice')
    print (fillings)
    p = get_object_or_404(Product, slug=product_slug)
    if not p.weight:
        weight = postdata.get('weight',0.96)
    else:
        weight = postdata.get('weight',p.weight)
    image = p.image
    print (weight)
    cart_products = get_cart_items(request)
    product_in_cart = False
    # check to see if item is already in cart
    for cart_item in cart_products:
        if cart_item.product.id == p.id and not cart_item.product.choice_weight:
            cart_item.augment_quantity(quantity)
            product_in_cart = True
    if not product_in_cart:   # create and save a new cart item
        ci = CartItem()
        ci.product = p
        if (description):
            ci.description = description
        if fillings:
            ci.filling = fillings
            print(ci.filling)
        ci.weight = weight
        ci.quantity = quantity
        ci.cart_id = _cart_id(request)
        ci.image = image
        ci.save()


def cart_distinct_item_count(request):
    """Общее число продуктов"""
    return get_cart_items(request).count()


def get_single_item(request, item_id):
    """Получаем CartItem"""
    return get_object_or_404(CartItem, id=item_id, cart_id=_cart_id(request))

# update quantity for single item
def update_cart(request):
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    quantity = postdata['quantity']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        if int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
        else:
            remove_from_cart(request)


# remove a single item from cart
def remove_from_cart(request):
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        cart_item.delete()


# gets the total cost for the current cart
def cart_subtotal(request):
    cart_total = 0
    cart_products = get_cart_items(request)
    for cart_item in cart_products:
        cart_total += float(cart_item.total)
    return cart_total


def is_empty(request):
    return cart_distinct_item_count(request) == 0


def empty_cart(request):
    user_cart = get_cart_items(request)
    user_cart.delete()