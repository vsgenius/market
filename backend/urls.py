from django.urls import path, include
from rest_framework import routers
from .views import PartnerUpdate
from .api import ProductViewSet, ShopProductViewSet, BasketViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register('product',ProductViewSet,'product')
router.register('shop',ShopProductViewSet,'shop')
router.register('basket',BasketViewSet,'basket')
urlpatterns = [
    path('',include(router.urls)),
    path('base_auth/',include('rest_framework.urls')),
    path('auth/',include('djoser.urls')),
    path('auth_token/',include('djoser.urls.authtoken'))

]
