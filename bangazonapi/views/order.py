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
        
    if request.query_params.get('completed', None) is not None:
      orders = orders.filter(completed = True)
    
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def update(self, request, pk):
    order = Order.objects.get(pk=pk)
    
    if 'customerId' in request.data:
      customer = User.objects.get(id=request.data['customerId'])
      order.customer = customer
    
    if 'paymentType' in request.data:
      order.payment_type = request.data['paymentType']
    
    if 'total' in request.data:  
      order.total = request.data['total']
      
    if 'tip' in request.data:  
      order.tip = request.data['tip']
      
    if 'orderType' in request.data:
      order.order_type = request.data['orderType']
    
    if 'dateCompleted' in request.data:
      order.date_completed = request.data['dateCompleted']
    
    if 'completed' in request.data:
      order.completed = request.data['completed']
    
    order.save()
    
    existing_order_items = Order_Item.objects.all().filter(order=order)
    if 'items' in request.data and existing_order_items.exists():
      for order_item in existing_order_items:
        order_item.delete()
    
    if 'items' in request.data:
      item_ids = request.data['items']
    
      for item_id in item_ids:
        item = Item.objects.get(id=item_id)
        Order_Item.objects.create(
          item = item,
          order = order
        )
    
    if 'items' in request.data:
      order = Order.objects.get(pk=pk)
      
    serializer = OrderSerializer(order)
    
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def create(self, request):
    customer = User.objects.get(id=request.data['customerId'])
    new_order = Order.objects.create(
        customer = customer,
        order_type = request.data['orderType'],
      )
    serializer = OrderSerializer(new_order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def destroy(self, request, pk):
    order = Order.objects.get(pk=pk)
    order.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
    

class OrderSerializer(serializers.ModelSerializer):
  customer = UserSerializer()
  items = serializers.SerializerMethodField(allow_null=True)
  class Meta:
    model = Order
    fields = ('id', 'customer', 'payment_type', 'total', 'tip', 'date_completed', 'completed', 'order_type', 'items')
    
  def get_items(self, obj):
    order_items = Order_Item.objects.all().filter(order=obj)
    items_list = [order_item.item for order_item in order_items]
    serializer = ItemSerializer(items_list, many=True)
    if len(items_list) > 0:
      return serializer.data
    else:
      return []