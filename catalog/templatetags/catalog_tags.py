from django import template
from catalog.models import Category, Filling, Product
from cart import cart
from catalog.models import LAST_PRODUCT

register = template.Library()

@register.inclusion_tag("tags/category_list.html")
def category_list(request_path):
    active_categories = Category.active.all()
    return { 'active_categories': active_categories, 'request_path': request_path }


@register.inclusion_tag("tags/cart_box.html")
def cart_box(request):
    cart_item_count = cart.cart_distinct_item_count(request)
    return {'cart_item_count': cart_item_count }

@register.inclusion_tag("tags/fillings.html")
def filling_list():
    fillings = Filling.active.all()
    return locals()

@register.inclusion_tag("tags/pop_products.html")
def pop_products_list():
    p = Product.object.filter(is_bestseller__exact = True)
    return {'pop_products':p[:2]}

@register.inclusion_tag("tags/last_products.html")
def last_products_list(request):
    p = []
    if LAST_PRODUCT in request.session:
        products_slug = request.session[LAST_PRODUCT]
        for s in products_slug:
            try:
                p.append(Product.object.get(slug__exact=s))
            except:
                pass
    return {'last_products':p[:2]}