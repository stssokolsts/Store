# -*- coding: utf-8 -*-
from django.db import models
import decimal


class CartItem(models.Model):
    cart_id = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1,blank=True, null=True)
    product = models.ForeignKey('catalog.Product', unique=False)
    description = models.TextField(blank=True, null=True)
    filling = models.CharField(max_length=250, blank=True, null=True)
    weight = models.FloatField()
    image = models.CharField(max_length=100)

    class Meta:
        db_table = 'cart_items'
        ordering = ['date_added']

    @property
    def total(self):
        if (self.product.choice_weight):
            print(self.weight)
            print(self.product.price)

            total =  float(self.weight)* float(self.product.price)
            print("total")
            print(total)
            return total
        else:
            return self.quantity * self.product.price

    def name(self):
        return self.product.name

    @property
    def price(self):
        return self.product.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def augment_quantity(self, quantity):
        self.quantity = self.quantity + int(quantity)
        self.save()

# Create your models here.
