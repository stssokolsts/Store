from django.contrib import admin
from models import Order, OrderItem

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'date', 'status', 'user','shipping')
    list_filter = ('status', 'date')
    search_fields = ('email', 'id' )
    inlines = [OrderItemInline,]
    fieldsets = (
                 ('Basics', {'fields': ('status','email','phone','shipping','address')}),
    )
admin.site.register(Order, OrderAdmin)
