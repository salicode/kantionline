from http import server
from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from django.http import HttpResponse 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Collection
from .serializer import ProductSerializer, CollectionSerializer 
# Create your views here.


@api_view(['GET', 'POST'])
def product_list(request):
   if request.method == 'GET':
    query_set = Product.objects.select_related('collection').all()
    serializer = ProductSerializer(query_set, many=True)
    return Response(serializer.data)
   elif  request.method == 'POST':
      serializer = ProductSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
     
     

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
 product = get_object_or_404(Product, pk=id)
 if request.method == 'GET':
      serializer = ProductSerializer(product)
      return Response(serializer.data)
 elif request.method == 'PUT':
      serializer = ProductSerializer(product, data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
 elif request.method == 'DELETE':
   if product.orderitems.count() > 0:
       return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
   product.delete()
   return Response({'error': 'Product can not be deleted because it is associated with an order item'}, status=status.HTTP_204_NO_CONTENT)
      
@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
          query_set = Collection.objects.annotate(products_count=Count('products')).all()
          serializer =CollectionSerializer(query_set, many=True)
          return Response(serializer.data)
    elif request.method == 'POST':
          serializer = CollectionSerializer(data=request.data)
          serializer.is_valid(raise_exception='True')
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk) 
     if request.method == 'GET':
           serializer = CollectionSerializer(collection)
           return Response(serializer.data)
     elif request.method == 'PUT':
           serializer = CollectionSerializer(Collection, data=request.data)
           serializer.is_valid(raise_exception='True')
           serializer.save()
           return Response(serializer.data)
     elif request == 'DELETE':
           if collection.products.count > 0:
                 return Response({'error', ''})
           collection.delete()
           return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)