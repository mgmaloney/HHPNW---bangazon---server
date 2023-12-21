from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from bangazonapi.models import Order, Item, User, Category, Order_Item
from .user import UserSerializer
from .item import ItemSerializer

class OrderView(ViewSet):
  """views for order"""
  def retrieve(self, request, pk):
    order = Order.objects.get(pk=pk)
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def list(self, request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def update(self, request, pk):
    order = Order.objects.get(pk=pk)
    
    order.payment_type = request.data['paymentType']
    order.total = request.data['total']
    order.shipping_address = request.data['shippingAddress']
    
    if request.data['dateCompleted'] is not None:
      order.date_completed = request.data['dateCompleted']
    
    if request.data['completed'] is not None:
      order.completed = request.data['completed']
    
    order.save()
    
    existing_order_items = Order_Item.objects.filter(order=order)
    if existing_order_items.exists():
      for order_item in existing_order_items:
        order_item.delete()
    
    item_ids = request.data['items']
    
    for item_id in item_ids:
      item = Item.objects.get(id=item_id)
      Order_Item.objects.create(
        item = item,
        order = order
      )
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)
    

class OrderSerializer(serializers.ModelSerializer):
  customer = UserSerializer()
  items = serializers.SerializerMethodField()
  class Meta:
    model = Order
    fields = ('id', 'customer', 'payment_type', 'total', 'shipping_address', 'date_completed', 'completed', 'items')
    
  def get_items(self, obj):
    order_items = Order_Item.filter(order=obj)
    items_list = [order_item.item for order_item in order_items]
    serializer = ItemSerializer(items_list, many=True)
    return serializer.data