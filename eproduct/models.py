#!-*-coding: utf-8 -*-
from django.db import models

class Brand(models.Model):
    title = models.CharField(max_length=200)

    def __unicode__(self):
        return u"%s: %s" % (self.id, self.title)

class Category(models.Model):
    text = models.CharField(max_length=200)

class Product(models.Model):
    title = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)
    brand = models.ForeignKey(Brand)

    def __unicode__(self):
        return u"%s: %s - %s" % (self.id, self.title, self.brand)

class FilterProductCrossIdCategoryBrand(models.Model):
    products = models.ManyToManyField(Product)
    categories = models.ManyToManyField(Category)
    brands = models.ManyToManyField(Brand)

    def has(self, product):
        if self.products.count() and product:
            if product not in self.products.all():
                #print 'not product'
                return False
        if self.categories.count() and product.categories.count():
            for category in product.categories.all():
                if category in self.categories.all():
                    break
            else:
                #print 'not category'
                return False
        if self.brands.count() and product.brand:
            if product.brand not in self.brands.all():
                #print 'not brand'
                return False
        return True



