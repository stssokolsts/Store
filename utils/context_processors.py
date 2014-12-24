from Store import settings
from accounts.models import UserProfile

#SOCIAL_PROVIDER = ""


def Store(request):
    """ context processor for the site templates """
    print(request.user)
    return {
            'site_name': settings.SITE_NAME,
            'meta_keywords': settings.META_KEYWORDS,
            'meta_description': settings.META_DESCRIPTION,
            'request': request,
            'user_name': get_user_name(request),
            'provider': get_provider(request),
            }


def get_provider(requset):
    try:
        p = requset.user.social_auth.values_list('provider')[0][0]
    except:
        p = ""
    return p

def get_user_name(request):
    username = ""
    if request.user.is_authenticated():
        try:
            username = request.user.userprofile.name
            print(username)
        except:
            username = ''
    return username