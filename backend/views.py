from django.http import JsonResponse
from .models import Shop, ShopProducts, Product, OrderProduct, Category, User
from rest_framework.views import APIView
from yaml import load as load_yaml, Loader


# Create your views here.


class PartnerUpdate(APIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if request.user.type != 'shop':
            return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        url = request.data.get('url')
        if url:
            with open(url, 'r') as stream:
                try:
                    data = load_yaml(stream, Loader=Loader)
                except:
                    print('Ошибка чтения')
                shop = Shop.objects.get_or_create(name=data['shop'], user_id=request.user.id)
                for category in data['categories']:
                    Category.objects.get_or_create(id=category['id'], name=category['name'], user_id=request.user.id)
                for item in data['goods']:
                    params = ''
                    for param in item['parameters']:
                        params += param+':'+str(item['parameters'][param])+ '\n'
                    product = Product.objects.get_or_create(external=item['id'],
                                                            name=item['name'],
                                                            model=item['model'],
                                                            category_id=item['category'],
                                                            user_id=request.user.id,
                                                            items=params)
                    print(product[0].id)
                    ShopProducts.objects.get_or_create(
                        price=item['price'],
                        price_rrc=item['price_rrc'],
                        quantity=item['quantity'],
                        product_id=product[0].id,
                        shop_id=shop[0].id,
                        user_id=request.user.id,
                    )

                return JsonResponse({'Status': True})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
