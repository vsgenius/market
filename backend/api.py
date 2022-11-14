from rest_framework.response import Response

from .serializers import *
from .models import *
from rest_framework import viewsets, permissions, status


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = CategorySerializers


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ProductSerializers


class ShopProductViewSet(viewsets.ModelViewSet):
    queryset = ShopProducts.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ShopProductSerializers

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data=[serializer.data,request.user.id]
        return Response(data)


class BasketViewSet(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = BasketSerializers

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = [serializer.data, request.user.id]
        return Response(data)

    def delete(self, request):
        id = request.data.get('id')
        OrderProduct.objects.filter(id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


