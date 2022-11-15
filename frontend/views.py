from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.views import View
from backend.models import User, Product, OrderProduct, Category, ShopProducts, Order
from frontend.forms import UserCreationForm, MyAuthentificationForm
from frontend.utils import verify_by_email, verify_order_by_email


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