from django import template
from accounts.forms import RegistrationForm, MyAuthenticationForm

register = template.Library()

@register.inclusion_tag("tags/register.html")
def register_modal():
    reg_form = RegistrationForm()
    auth_form = MyAuthenticationForm()
    return {'reg_form': reg_form, 'auth_form' : auth_form}