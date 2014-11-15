from models import SearchTerm
from catalog.models import Product
from django.db.models import Q


def store(request, q):
 # if search term is at least three chars long, store in db 
    if len(q) > 2:
        term = SearchTerm()
        term.q = q
        term.ip_address = request.META.get('REMOTE_ADDR')
        term.user = None
        term.save()


def products(search_text):
    results = []
    print(list(results))
    results['products'] = Product.search.query(search_text)
    print(list(results))
    return results


def products_def(search_text):
    """ get products matching the search text """
    words = _prepare_words(search_text)
    products = Product.active.all()
    results = {}
    for word in words:
        products = products.filter(Q(name__icontains=word) |
        Q(description__icontains=word) |
        Q(brand__icontains=word) |
        Q(meta_keywords__icontains=word))
        results['products'] = products
    return results


def _prepare_words(search_text):
    """ strip out common words, limit to 5 words """
    words = search_text.split()
    return words[0:5]