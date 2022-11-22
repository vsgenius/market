from rest_framework import serializers
from .models import *


class CategorySerializers(serializers.ModelSerializer):
    products = serializers.StringRelatedField(many=True,read_only=True)
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault)

    class Meta:
        model = Category
        fields = '__all__'


class ShopSerializers(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault)

    class Meta:
        model = Shop
        fields = '__all__'


class ProductSerializers(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault)
    category_name = serializers.ReadOnlyField(source='category.name')
    class Meta:
        model = Product
        fields = '__all__'


class ShopProductSerializers(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault)
    product_name = serializers.ReadOnlyField(source='product.name')
    product_id = serializers.ReadOnlyField(source='product.pk')
    product_model = serializers.ReadOnlyField(source='product.model')
    category = serializers.ReadOnlyField(source='product.category.name')
    shop_name = serializers.ReadOnlyField(source='shop.name')
    shop_id = serializers.ReadOnlyField(source='shop.pk')
    user_id = serializers.ReadOnlyField(source='user.pk')

    class Meta:
        model = ShopProducts
        fields = '__all__'


class BasketSerializers(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_model = serializers.ReadOnlyField(source='product.model')
    category = serializers.ReadOnlyField(source='product.category.name')
    shop_name = serializers.ReadOnlyField(source='shop.name')
    user_id = serializers.ReadOnlyField(source='user.pk')

    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrdersSerializers(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'