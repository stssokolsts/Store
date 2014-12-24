

def set_last_product(request, product_slug):
    if "last_products" in request.session:
        l = len(request.session["last_products"])
        if product_slug not in request.session["last_products"]:
            if l == 1:
                request.session["last_products"].append(product_slug)
            else:
                request.session["last_products"][0], request.session["last_products"][1] \
                    = request.session["last_products"][1], product_slug
    else:
        request.session["last_products"] = []
        request.session["last_products"].append(product_slug)