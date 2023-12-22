from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.db.models import Q
from bangazonapi.models import User, Order, Order_Item
from .item import ItemSerializer

class UserView(ViewSet):
  @action(methods=['POST'], detail=True)
  def has_order(self, request, pk):
    customer = User.objects.get(pk=pk)
    order_query = Order.objects.filter(Q(customer=customer) & Q(completed=False))
    if order_query.exists():
      assert len(order_query) == 1
      if len(order_query) == 1:
        order = list(order_query)[0]
        serializer = OrderSerializer(order)
      
      return Response(serializer.data, status=status.HTTP_200_OK)
    
    else:
      new_order = Order.objects.create(
        customer = customer,
      )
      return Response(None, status=status.HTTP_201_CREATED)

    



class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'uid', 'first_name', 'last_name', 'bio', 'email', 'address', 'phone_number', 'is_seller')

class OrderSerializer(serializers.ModelSerializer):
  customer = UserSerializer()
  class Meta:
    model = Order
    fields = ('id', 'customer', 'payment_type', 'total', 'shipping_address', 'date_completed', 'completed')