from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import Item, Category
from .category import CategorySerializer

class ItemView(ViewSet):
  """views for item"""
  def retrieve(self, request, pk):
    item = Item.objects.get(pk=pk)
    serializer = ItemSerializer(item, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def list(self, request):
    items = Item.objects.all()    
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def create(self, request):
    category = Category.objects.get(id=request.data['categoryId'])
    item = Item.objects.create(
      name = request.data['name'],
      price = request.data['price'],
      image_url = request.data['imageUrl'],
      category = category,
    )
    serializer = ItemSerializer(item, many=False)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def update(self, request, pk):
    category = Category.objects.get(id=request.data['categoryId'])
    item = Item.objects.get(pk=pk)
    
    item.name = request.data['name']
    item.price = request.data['price']
    item.image_url = request.data['imageUrl']
    item.category = category

    item.save()
    
    serializer = ItemSerializer(item, many=False)
    
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def destroy(self, request, pk):
    item = Item.objects.get(pk=pk)
    item.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)

class ItemSerializer(serializers.ModelSerializer):
  category = CategorySerializer(many=False)
  class Meta:
    model = Item
    fields = ('id', 'name', 'price', 'image_url', 'category')