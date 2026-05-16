from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, User, Users
from .serializers import ProductSerializers, UserSerializers, UsersSerializers


# 1) Product qo'shish
@api_view(['POST'])
def product_create(request):
    serializers = ProductSerializers(data=request.data)

    if serializers.is_valid():
        serializers.save()
        return Response(serializers.data)

# 2) Product o'chirish
@api_view(['DELETE'])
def product_delete(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()

    return Response({'message': "Deleted"})

# 3) Bitta product olish
@api_view(['GET'])
def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    serializers = ProductSerializers(product)
    return Response(serializers.data)

# 4) Hamma productlarni olish
@api_view(['GET'])
def product_list(request):
    product = Product.objects.all()
    serializers = ProductSerializers(product, many=True)
    return Response(serializers.data)

# 5) Productni yangilash
@api_view(['PUT'])
def product_update(request, pk):
    product = Product.objects.get(id=pk)
    serializers = ProductSerializers(product, data=request.data)

    if serializers.is_valid():
        serializers.save()
        return Response(serializers.data)

class UserList(APIView):
    def get(self, request):
        user = User.objects.all()
        serializers = UserSerializers(user, many=True)
        return Response(serializers.data)

    def post(self, request):
        serializers = UserSerializers(data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=201)

        return Response(serializers.errors, status=400)

class UsersLists(
        generics.GenericAPIView,
        mixins.DestroyModelMixin
    ):

    queryset = Users.objects.all()
    serializer_class = UsersSerializers

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        return self.destroy(request, pk)






