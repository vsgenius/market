from django.urls import path, include
from django.views.generic import TemplateView

from frontend.utils import verify_order_by_email
from frontend.views import MyLoginView, EmailVerify, Register, home, basket, orders, OrderVerify, CreateOrder

urlpatterns = [
    path('login/', MyLoginView.as_view(),name='login'),
    path('',include('django.contrib.auth.urls')),
    path('invalid_verify/',TemplateView.as_view(template_name='registration/invalid_verify.html'),
         name='invalid_verify'),
    path('success_verify/', TemplateView.as_view(template_name='registration/success_verify.html'),
         name='success_verify'),
    path('send_email/', TemplateView.as_view(template_name='registration/send_email.html'),
         name='send_email'),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(),name='verify_email'),
    path('verify_order/<order_id>/<uidb64>/<token>/', OrderVerify.as_view(), name='verify_order'),
    path('register/',Register.as_view(), name = 'register'),
    path('', home, name='home'),
    path('basket/', basket, name='basket'),
    path('orders/', orders, name='orders'),
    path('order_send_email/<id>',CreateOrder.as_view(),name='order_send_email'),
    path('create_order/', TemplateView.as_view(template_name='create_order.html'), name='create_order'),
    path('verify_order_by_email/', TemplateView.as_view(template_name='verify_order_by_email.html'),
         name='verify_order_by_email'),
    path('invalid_verify_order/', TemplateView.as_view(template_name='invalid_verify_order.html'),
         name='invalid_verify_order'),
]