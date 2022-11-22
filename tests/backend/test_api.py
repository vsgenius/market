import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from backend.models import User, Category, Product, ShopProducts, Shop, OrderProduct


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user('admin')


@pytest.fixture
def category(user):
    return Category.objects.create(name='name',user_id=user.id)


@pytest.fixture
def product(user,category):
    return Product.objects.create(external=1,
                                    name="name",
                                    model="model",
                                    items= "items",
                                    user_id=user.id,
                                    category_id=category.id)


@pytest.fixture
def shop(user):
    return Shop.objects.create(name="name",
                                url="url",
                                user_id=user.id
                                  )


@pytest.fixture
def shop_product(user,product,shop):
    return ShopProducts.objects.create(price=1,
                                price_rrc=1,
                                quantity=1,
                                shop_id=shop.id,
                                product_id=product.id,
                                user_id=user.id
                                  )
@pytest.fixture
def product_factory():
    def factory(*args,**kwargs):
        return baker.make(Product,*args,**kwargs)

    return factory


@pytest.fixture
def cat_factory():
    def factory(*args,**kwargs):
        return baker.make(Category,*args,**kwargs)

    return factory


@pytest.fixture
def shop_product_factory():
    def factory(*args,**kwargs):
        return baker.make(ShopProducts,*args,**kwargs)

    return factory


@pytest.fixture
def basket_factory():
    def factory(*args,**kwargs):
        return baker.make(OrderProduct,*args,**kwargs)

    return factory


@pytest.mark.django_db
def test_categories(client,cat_factory):
    cat = cat_factory(_quantity=100)
    response = client.get('/api/v1/categories/')
    data=response.json()
    assert len(data)==len(cat)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_categories(client,user):
    count = Category.objects.count()
    content = {
    'name': "name",
    'user':user.id
    }
    response = client.post('/api/v1/categories/',data=content)
    assert response.status_code == 201
    assert count==Category.objects.count()-1


@pytest.mark.django_db
def test_product(client,product_factory):
    products = product_factory(_quantity=100)
    response = client.get('/api/v1/product/')
    data=response.json()
    assert len(data)==len(products)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_product(client,user,category):
    count = Product.objects.count()
    content = {
    "external": 1,
    "name": "name",
    "model": "model",
    "items": "items",
    "user": user.id,
    "category": category.id
}
    response = client.post('/api/v1/product/',data=content, format='json')
    assert response.status_code == 201
    assert count==Product.objects.count()-1


@pytest.mark.django_db
def test_shop(client,shop_product_factory):
    shop_products = shop_product_factory(_quantity=100)
    response = client.get('http://127.0.0.1:8000/api/v1/shop/')
    data=response.json()
    assert len(data[0])==len(shop_products)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_shop(client,user,product,shop):
    count = ShopProducts.objects.count()
    content = {
    "price": 1,
    "price_rrc": 2,
    "quantity": 1,
    "shop": shop.id,
    "product": product.id,
    "user": user.id,
}
    response = client.post('/api/v1/shop/',data=content, format='json')
    assert response.status_code == 201
    assert count==Product.objects.count()-1


@pytest.mark.django_db
def test_basket(client):
    response = client.get('/api/v1/basket/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_basket(client,user,product,shop,shop_product):
    count = OrderProduct.objects.count()
    content = {
    "order": 0,
    "quantity": 1,
    "price": 1,
    "product": product.id,
    "shop": shop.id,
    "shop_products": shop_product.id,
    "user": user.id
}
    response = client.post('/api/v1/basket/',data=content, format='json')
    assert response.status_code == 201
    assert count==Product.objects.count()-1

