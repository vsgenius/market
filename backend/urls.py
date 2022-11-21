from django.urls import path, include
from rest_framework import routers
from .views import PartnerUpdate
from .api import ProductViewSet, ShopProductViewSet, BasketViewSet, CategoryViewSet, OrdersViewSet

router = routers.DefaultRouter()
router.register('product',ProductViewSet,'product')
router.register('shop',ShopProductViewSet,'shop')
router.register('basket',BasketViewSet,'basket')
router.register('orders',OrdersViewSet,'orders')
urlpatterns = [
    path('',include(router.urls)),
    path('base_auth/',include('rest_framework.urls')),
    path('auth/',include('djoser.urls')),
    path('auth_token/',include('djoser.urls.authtoken')),
    path('load_products/',PartnerUpdate.as_view(),name='load_products'),

]
