#!-*-coding: utf-8 -*-
from django.db import models

class Brand(models.Model):
    title = models.CharField(max_length=200)

class Category(models.Model):
    text = models.CharField(max_length=200)

class Product(models.Model):
    text = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)
    brand = models.ForeignKey(Brand)

class FilterProductCrossIdCategoryBrand(models.Model):
    products = models.ManyToManyField(Product)
    categories = models.ManyToManyField(Category)
    brands = models.ManyToManyField(Brand)



