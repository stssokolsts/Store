from django import template
from accounts.forms import RegistrationForm, MyAuthenticationForm

register = template.Library()

@register.inclusion_tag("tags/register.html")
def register_modal():
    reg_form = RegistrationForm()
    auth_form = MyAuthenticationForm()
    return {'reg_form': reg_form, 'auth_form' : auth_form}

@register.inclusion_tag("tags/accounts_info.html")
def accounts_info(request):
    try:
        p = request.user.social_auth.values_list('provider')[0][0]
    except:
        p = ""
    username = ""
    if request.user.is_authenticated():
        try:
            username = request.user.userprofile.name
            print(username)
        except:
            username = ''
    return {'provider':p, 'user_name': username}