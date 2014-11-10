from models import SearchTerm
from catalog.models import Product

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