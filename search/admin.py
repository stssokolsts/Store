from django.contrib import admin
from models import SearchTerm


class SearchTermAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','ip_address','search_date')
    list_filter = ('ip_address', 'q', 'user')
    exclude = ('user',)

admin.site.register(SearchTerm, SearchTermAdmin)
# Register your models here.
