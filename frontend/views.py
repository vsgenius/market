from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.views import View
from backend.models import User, Product, OrderProduct, Category, ShopProducts, Order
from frontend.forms import UserCreationForm, MyAuthentificationForm
from frontend.utils import verify_by_email, verify_order_by_email

User = get_user_model()


def category(request):
    user = request.user
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'create_product.html', context)


def orders(request):
    user = request.user
    orders = Order.objects.all()
    context = {'products': orders}
    return render(request, 'orders.html', context)


def create_order(request):
    verify_order_by_email()
    context = {}
    return render(request, 'orders.html', context)


def basket(request):
    user = request.user
    products = OrderProduct.objects.filter(user_id=user.pk)
    context = {'products': products,
               'count':len(products)}
    return render(request, 'basket.html', context)


def home(request):
    user = request.user
    products = ShopProducts.objects.filter(user_id=user.pk)
    categories = Category.objects.all()
    orders = len(OrderProduct.objects.filter(user_id=user.pk))
    context = { 'products':products,
                'categories':categories,
               'count_order':orders}
    return render(request, 'home.html', context)


class LoginAjaxView(View):

    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user =authenticate(email=email,password=password)
            if user:
                login(request,user)

                return JsonResponse(data={},status=201)
            return JsonResponse(data={'error':'Email or Pass not valid'}, status=400)
        return JsonResponse(data={'error': 'Email or Pass is Empty'}, status=400)


class CreateAjaxView(View):

    def post(self,request):
        user = request.user.id
        external_id = request.POST.get('external_id')
        model = request.POST.get('model')
        name = request.POST.get('name')
        category = request.POST.get('category')
        items = request.POST.get('items')
        if request.user.type=='shop' or request.user.type=='stuff':
                return JsonResponse(data={},status=201)
        return JsonResponse(data={'error':'Нет доступа'}, status=400)


class MyLoginView(LoginView):
    form_class = MyAuthentificationForm


class EmailVerify(View):

    def get(self,request,uidb64,token):
        user = self.get_user(uidb64)
        if user is not None and default_token_generator.check_token(user,token):
            user.is_email_active = True
            user.save()
            login(request,user)
            return redirect('success_verify')
        return redirect('invalid_verify')


    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,User.DoesNotExist,ValidationError):
            user = None
        return user


class OrderVerify(View):

    def get(self,request,uidb64,token,order_id):
        user = self.get_user(uidb64)
        if user is not None and default_token_generator.check_token(user,token):
            orders = Order.objects.get(pk=order_id,user_id=user.pk)
            if orders.pk is None:
                verify_order_by_email(request, order_id)
                return redirect('invalid_verify_order')
            orders.status = 'confirmed'
            orders.save()
            return redirect('verify_order_by_email')
        verify_order_by_email(request,order_id)
        return redirect('invalid_verify_order')


    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,User.DoesNotExist,ValidationError):
            user = None
        return user


class CreateOrder(View):
    template_name = 'create_order.html'

    def get(self,request,id):
        context = {}
        verify_order_by_email(request,id)
        return redirect('create_order')

    def post(self,request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(password=password,username=email)
            # login(request,user)
            verify_by_email(request,user)
            return redirect('create_order')
        context = {
            'form':form
        }
        return render(request,self.template_name,context)


class Register(View):
    template_name = 'registration/register.html'

    def get(self,request):
        context = {
            'form':UserCreationForm()
        }
        return render(request,self.template_name,context)

    def post(self,request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(password=password,username=email)
            # login(request,user)
            verify_by_email(request,user)
            return redirect('send_email')
        context = {
            'form':form
        }
        return render(request,self.template_name,context)