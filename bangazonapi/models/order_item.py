from django.db import models
from .order import Order
from .item import Item

class Order_Item(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)