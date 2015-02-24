# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product, Filling


SHIPPING_CHOICES = (('1', 'Самовывоз',), ('2', 'Бесплатная доставка',))
BILLING_CHOICES = (('1', 'Наличный/безналичный рассчет в магазине "Вкусный праздник"',),
                   ('2', 'Электронная коммерция (30%) *',),('3', 'Электронная коммерция (100%) *',))

class BaseOrderInfo(models.Model):
    class Meta:
        abstract = True
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=150)


class Order(BaseOrderInfo):
    """ model class for storing a customer order instance """
    # each individual status
    SUBMITTED = 1
    PROCESSED = 2
    SHIPPED = 3
    CANCELLED = 4
    # set of possible order statuses
    ORDER_STATUSES = ((SUBMITTED,'Submitted'),
                      (PROCESSED,'Processed'),
                      (SHIPPED,'Shipped'),
                      (CANCELLED,'Cancelled'),)
    #order info
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    ip_address = models.IPAddressField()
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True)
    email = models.EmailField(max_length=70)
    shipping = models.CharField(max_length=30, choices=SHIPPING_CHOICES, default=SHIPPING_CHOICES[0][0])
    billing = models.CharField(max_length=50, choices=BILLING_CHOICES, default=BILLING_CHOICES[0][0])
    address = models.CharField(max_length=250, null=True,blank=True)

    def __unicode__(self):
        return u'Order #' + str(self.id)

    @property
    def total(self):
        total = 0
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.total
            print(item.total)
        print(total)
        return total

    @models.permalink
    def get_absolute_url(self):
        return ('order_details', (), {'order_id': self.id})


class OrderItem(models.Model):
    """ model class for storing each Product instance purchased in each order """
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)
    weight = models.FloatField()
    filling = models.CharField(null=True, max_length=250)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    order = models.ForeignKey(Order)

    @property
    def total(self):
        if self.weight:
            return self.weight * float(self.product.price)
        else:
            return self.quantity*float(self.price)

    #@property
    #def price(self):
        #return self.product.price

    @property
    def name(self):
        return self.product.name

    #@property
    #def sku(self):
     #   return self.product.

    def __unicode__(self):
        return self.product.name

    def get_absolute_url(self):
        return self.product.get_absolute_url()