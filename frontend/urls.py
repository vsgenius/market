from django.urls import path, include
from django.views.generic import TemplateView

from frontend.views import MyLoginView, EmailVerify, Register, home, basket

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
    path('register/',Register.as_view(), name = 'register'),
    path('', home, name='home'),
    path('basket/', basket, name='basket'),
]