from django.contrib import admin
from .models import OrderProduct, Product, Category, Shop, ShopProducts


# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    extra = 1


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    model = Shop
    extra = 1


@admin.register(ShopProducts)
class ShopProductsAdmin(admin.ModelAdmin):
    model = ShopProducts
    extra = 1


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    model = OrderProduct
    extra = 1
