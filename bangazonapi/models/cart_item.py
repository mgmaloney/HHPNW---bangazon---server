from django.db import models
from .cart import Cart
from .item import Item

class Cart_Item(models.Model):
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)