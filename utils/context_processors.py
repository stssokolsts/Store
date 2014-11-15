from Store import settings

def Store(request):
    """ context processor for the site templates """
    return {
            'site_name': settings.SITE_NAME,
            'meta_keywords': settings.META_KEYWORDS,
            'meta_description': settings.META_DESCRIPTION,
            'request': request
            }
