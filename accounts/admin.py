from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from models import UserProfile

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserInline(admin.StackedInline):
    model = UserProfile
    #list_display = ('name',)
    can_delete = False
    verbose_name_plural = 'employee'

# Define a new User admin
class UserProfileAdmin(UserAdmin):
    inlines = (UserInline, )
    list_display = ('email','is_staff')


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)