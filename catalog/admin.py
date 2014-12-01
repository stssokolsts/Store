from django.contrib import admin
from catalog.models import Product, Category, Filling, Brand
from catalog.forms import ProductAdminForm


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    # sets values for how the admin site lists your products
    list_display = ('name', 'price', 'old_price', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 50
    ordering = ['-created_at']
    search_fields = ['name', 'description', 'meta_keywords','meta_description',]
    exclude = ('created_at', 'updated_at',)
    # sets up slug to be generated from product name
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    #sets up values for how admin site lists categories
    list_display = ('name', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    exclude = ('created_at', 'updated_at',)
    # sets up slug to be generated from category name
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

class FillingAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image',)
    ordering = ('name',)

admin.site.register(Filling,FillingAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'image',)
    ordering = ('name',)

admin.site.register(Brand,BrandAdmin)