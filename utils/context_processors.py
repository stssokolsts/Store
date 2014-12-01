from Store import settings
from accounts.models import UserProfile

def Store(request):
    """ context processor for the site templates """
    try:
        username = UserProfile.objects.get(id = request.user.id).name
    except:
        username = ''
    return {
            'site_name': settings.SITE_NAME,
            'meta_keywords': settings.META_KEYWORDS,
            'meta_description': settings.META_DESCRIPTION,
            'request': request,
            'user_name': username
            }
