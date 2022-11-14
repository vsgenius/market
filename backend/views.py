from django.http import JsonResponse
from .models import Shop,ShopProducts,Product,OrderProduct,Category,User
from rest_framework.views import APIView
from yaml import load as load_yaml,Loader
# Create your views here.


class PartnerUpdate(APIView):
    def post(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        #
        # if request.user.type != 'shop':
        #     return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        url = request.data.get('url')
        if url:
            with open(url, 'r') as stream:
                try:
                    data = load_yaml(stream, Loader=Loader)
                except:
                    print('Ошибка чтения')
                shop = Shop.objects.get_or_create(name=data['shop'], user_id=request.user.id)
                for category in data['categories']:
                    category_object = Category.objects.get_or_create(id=category['id'], name=category['name'])
                    category_object.shops.add(shop.id)
                    category_object.save()
                # ProductInfo.objects.filter(shop_id=shop.id).delete()
                for item in data['goods']:
                    product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])
                    product_info = Product.objects.create(product_id=product.id,
                                                              external_id=item['id'],
                                                              model=item['model'],
                                                              price=item['price'],
                                                              price_rrc=item['price_rrc'],
                                                              quantity=item['quantity'],
                                                              shop_id=shop.id)
                    for name, value in item['parameters'].items():
                        parameter_object, _ = Product.objects.get_or_create(name=name)
                        Product.objects.create(product_info_id=product_info.id,
                                                        parameter_id=parameter_object.id,
                                                        value=value)

                return JsonResponse({'Status': True})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

