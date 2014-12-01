# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from checkout.models import BaseOrderInfo
from catalog.models import Product

class UserProfile(BaseOrderInfo):
    """ Расширение стандартного класса User для хранения дополнительных полей"""
    user = models.OneToOneField(User)
    favorites = models.ManyToManyField(Product, null=True)

    def __unicode__(self):
        return 'User Profile for: ' + self.user.username