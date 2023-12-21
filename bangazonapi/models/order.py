from django.db import models

class Order(models.Model):
  cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
  customer = models.ForeignKey(User, on_delete=models.PROTECT)
  payment_type = models.CharField(max_length=30, default='')
  total = models.DecimalField(default=0, max_digits=10, decimal_places=2),
  shipping_address = models.CharField(max_length=250),
  date_completed = models.DateTimeField(auto_now_add=True)