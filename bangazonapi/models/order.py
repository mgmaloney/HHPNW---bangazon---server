from django.db import models
from .user import User

class Order(models.Model):
  customer = models.ForeignKey(User, on_delete=models.PROTECT)
  order_type = models.CharField(max_length=250, default='')
  date_completed = models.DateTimeField(blank=True, null=True)
  completed = models.BooleanField(default=False)
  payment_type = models.CharField(max_length=30, default='')
  total = models.DecimalField(default=0, max_digits=10, decimal_places=2)
  tip = models.DecimalField(default=0, max_digits=10, decimal_places=2)