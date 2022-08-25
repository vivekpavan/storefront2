from re import T
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action;
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from store.filters import ProductFilter
from store.pagination import PaginationClass
from .models import Cart, CartItem, Customer, OrderItem, Product,Collection, Review
from .serializer import AddCartItemSerializer, CartItemSerializer, CartSerializer, CollectionSerializer, CustomerSerializer, ProductSerializer, ReviewSerializer, UpdateCartItemSerializer
from store import serializer

# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = PaginationClass

    search_fields = ['title','description']
    ordering_fields = ['unit_price','last_update']

    def get_serializer_context(self):
        return {'request' : self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error':'Product cannot can not be deleted'},status = status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)
    
class ReviewViewSet(ModelViewSet):
    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'])

    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}

# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(
#         products_count=Count('products')).all()
#     serializer_class = CollectionSerializer

# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(
#         products_count = Count('products')
#     )
#     serializer_class = CollectionSerializer

#     def delete(Self,request,pk):
#         collection = get_object_or_404(Collection,pk = pk)
#         if collection.products.count() > 0:
#             return Response({'error':'Collection cannot be deleted'})
#         collection.delete() 
#         return Response(status=status.HTTP_204_NO_CONTENT)

class CartViewSet(CreateModelMixin,GenericViewSet,RetrieveModelMixin,DestroyModelMixin):

    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id' : self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects\
        .filter(cart_id = self.kwargs['cart_pk'])\
        .select_related('product')

class CustomerViewSet(CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    @action(detail=False,methods=['GET','PUT'])
    def me(self,request):
        return Response(request.user.id)