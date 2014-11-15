from django.db import models
from djangosphinx.models import SphinxSearch
from django.db.models.signals import post_save, post_delete
from caching.caching import cache_update, cache_evict

class ActiveCategoryManager(models.Manager):
    def get_query_set(self):
        return super(ActiveCategoryManager, self).get_query_set().filter(is_active=True)


class ActiveProductManager(models.Manager):
    def get_query_set(self):
        return super(ActiveProductManager, self).get_query_set().filter(is_active=True)

class ActiveFillingManager(models.Manager):
    def get_query_set(self):
        return super(ActiveFillingManager,self).get_query_set().filter(is_active=True)


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True,
                            help_text= 'Unique value for product page URL, created from name.')
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta Keywords",max_length=255,
                                     help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField("Meta Description", max_length=255,
                                        help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    active = ActiveCategoryManager()
    detail = models.BooleanField(default=True)
    image = models.ImageField(upload_to='image/categories')

    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('catalog_category', (), {'category_slug': self.slug})

    @property
    def cache_key(self):
        return self.get_absolute_url()


class Product(models.Model):
    """ model class containing information about a product; instances of this class are what the user
    adds to their shopping cart and can subsequently purchase

    """
    #featured = FeaturedProductManager()
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True,
                            help_text='Unique value for product page URL, created automatically from name.')
    brand = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    old_price = models.DecimalField(max_digits=9,decimal_places=2,
                                    blank=True,default=0.00)
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    #quantity = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    #min_weight = models.IntegerField(blank =True, null=True)
    #max_weight = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    meta_keywords = models.CharField("Meta Keywords",max_length=255,
                                     help_text='Comma-delimited set of SEO keywords for keywords meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)

    image = models.ImageField(upload_to='image/products/thumbnails')
    #thumbnail = ThumbnailImageFields(upload_to='images/products/thumbnails')
    image_caption = models.CharField(max_length=100)
    object = models.Manager()
    active = ActiveProductManager()
    choice_weight = models.BooleanField(default=False)

    search = SphinxSearch(weight={
        'name': 100,
        'brand' :80,
        'description': 60,
        'meta_keywords': 50},
                          mode='SPH_MATCH_ANY')

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('catalog_product', (), { 'product_slug': self.slug })

    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None

    @property
    def cache_key(self):
        return self.get_absolute_url()


class Filling(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='image/filling', blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'fillings'
        ordering = ['-name']

    def __unicode__(self):
        return self.name

    objects = models.Manager()
    active = ActiveFillingManager()

class Brand(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='image/brands')

post_save.connect(cache_update, sender=Product)
post_delete.connect(cache_evict, sender=Product)
post_save.connect(cache_update, sender=Category)
post_delete.connect(cache_evict, sender=Category)

