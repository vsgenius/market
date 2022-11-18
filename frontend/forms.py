from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import (UserCreationForm as MyUserCreationForm, AuthenticationForm)
from django import forms
from django.core.exceptions import ValidationError

from backend.models import USER_TYPE_CHOICES, Category
from .utils import verify_by_email


User = get_user_model()


def get_categories():
    categories = Category.objects.all()
    result = []
    for category in categories:
        result.append((category.id, category.name))
    return result


class AuthenticationAjaxForm(forms.Form):
    email = forms.EmailField(
        label=('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autocomlete': 'email',
            'class':'form-control'})
    )
    password = forms.CharField(
        label=('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomlete': 'current-password',
            'class':'form-control'})
    )


class CreateProductForm(forms.Form):
    external = forms.IntegerField(
        label=('Внешний ИД'),
        widget=forms.TextInput(attrs={
                                       'class':'form-control'})
    )
    name = forms.CharField(
        label=('Наименование'),
        max_length=254,
        widget=forms.TextInput(attrs={
                                      'class': 'form-control'})

    )
    model = forms.CharField(
        label=('Модель'),
        max_length=254,
        widget=forms.TextInput(attrs={
                                      'class': 'form-control'})
    )
    category = forms.ChoiceField(
        label=('Категория'),
        choices=get_categories(),
        widget=forms.Select(attrs={"class": "form-select"})
    )
    items = forms.CharField(
        label=('Параметры'),
        widget=forms.Textarea(attrs={"class": "form-control"}))
    user = forms.IntegerField(
        widget=forms.HiddenInput(),
        initial=User.pk
    )


class MyAuthentificationForm(AuthenticationForm):
    username = forms.CharField(
        label=('Username'),
        max_length=254,
        widget=forms.TextInput(attrs={'autocomlete': 'username',
                                       'class':'form-control'})
    )
    password = forms.CharField(
        label=('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomlete': 'current-password',
            'class':'form-control'})
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                username=username,
                password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
            if not self.user_cache.is_email_active:
                verify_by_email(self.request,self.user_cache)
                raise ValidationError(
                    'Электронная почта не подтверждена. Ссылка направлена повторно.',
                    code='invalid_verify'
                )

        return self.cleaned_data


class UserCreationForm(MyUserCreationForm):
    username = forms.CharField(
        label=('Username'),
        max_length=254,
        widget=forms.TextInput(attrs={'autocomlete': 'username',
                                       'class':'form-control'})
    )
    email = forms.EmailField(
        label=('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomlete': 'email',
                                       'class':'form-control'})
    )
    password1 = forms.CharField(
        label=('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomlete': 'current-password',
            'class':'form-control'})
    )
    password2 = forms.CharField(
        label=('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomlete': 'current-password',
            'class':'form-control'})
    )
    type = forms.ChoiceField(
        label=('Type'),
        choices=USER_TYPE_CHOICES,
    widget=forms.Select(attrs={"class":"form-select"}))

    class Meta(MyUserCreationForm.Meta):
        model = User
        fields = ('username', 'email')
