from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_rest_passwordreset.tokens import get_token_generator

STATE_CHOICES = (
    ('basket', 'Статус корзины'),
    ('confirmed', 'Подтвержден'),
    ('new','Новый'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)

USER_TYPE_CHOICES = (
    ('shop', 'Магазин'),
    ('buyer', 'Покупатель'),
    ('stuff', 'Сотрудник'),

)


class UserManager(BaseUserManager):
    """
    Миксин для управления пользователями
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Стандартная модель пользователей
    """
    REQUIRED_FIELDS = ['username']
    objects = UserManager()
    USERNAME_FIELD = 'email'
    email = models.EmailField(_('email address'), unique=True)
    company = models.CharField(verbose_name='Компания', max_length=40, blank=True)
    position = models.CharField(verbose_name='Должность', max_length=40, blank=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_email_active = models.BooleanField(
        default=False)
    type = models.CharField(verbose_name='Тип пользователя', choices=USER_TYPE_CHOICES, max_length=5, default='buyer')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Список пользователей"
        ordering = ('email',)


class ConfirmEmailToken(models.Model):
    class Meta:
        verbose_name = 'Токен подтверждения Email'
        verbose_name_plural = 'Токены подтверждения Email'

    @staticmethod
    def generate_key():
        """ generates a pseudo random code using os.urandom and binascii.hexlify """
        return get_token_generator().generate_token()

    user = models.ForeignKey(
        User,
        related_name='confirm_email_tokens',
        on_delete=models.CASCADE,
        verbose_name=_("The User which is associated to this password reset token")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("When was this token generated")
    )

    # Key field, though it is not the primary key of the model
    key = models.CharField(
        _("Key"),
        max_length=64,
        db_index=True,
        unique=True
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ConfirmEmailToken, self).save(*args, **kwargs)

    def __str__(self):
        return "Password reset token for user {user}".format(user=self.user)


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование')
    user = models.ForeignKey(User, related_name='categories',verbose_name='Пользователь', on_delete=models.CASCADE, auto_created=True)
    create_at = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    external = models.IntegerField(verbose_name='Внешний ИД')
    name = models.CharField(max_length=100, verbose_name='Наименование')
    model = models.CharField(max_length=50, verbose_name='Модель')
    category = models.ForeignKey(Category, verbose_name='Категория',
                                    on_delete=models.CASCADE,related_name='products')
    items = models.TextField(verbose_name='Параметры')
    user = models.ForeignKey(User,related_name='products', verbose_name='Пользователь',
                             on_delete=models.CASCADE, auto_created=True)
    create_at = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Shop(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование')
    url = models.URLField(verbose_name='Сайт')
    user = models.ForeignKey(User,verbose_name='shops', on_delete=models.CASCADE,auto_created=True)
    create_at = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


class ShopProducts(models.Model):
    shop = models.ForeignKey(Shop, related_name='ShopProducts',verbose_name='Магазин', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='ShopProducts',verbose_name='Товар', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(verbose_name='Цена')
    price_rrc = models.PositiveIntegerField(verbose_name='Розничная цена')
    quantity = models.IntegerField()
    user = models.ForeignKey(User, verbose_name='ShopProducts', on_delete=models.CASCADE, auto_created=True)
    create_at = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        verbose_name = 'Товары в магазине'
        verbose_name_plural = 'Товары в магазинах'


class Order(models.Model):
    status = models.CharField(max_length=50, choices=STATE_CHOICES)
    user = models.ForeignKey(User, related_name='Ordeк',verbose_name='Пользователь', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    modified = models.DateTimeField(auto_created=True, auto_now=True)
    price = models.PositiveIntegerField(verbose_name='Цена')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderProduct(models.Model):
    order = models.IntegerField(blank=True)
    product = models.ForeignKey(Product, related_name='OrderProducts',verbose_name='Товар', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop,related_name='OrderProducts', verbose_name='Магазин', on_delete=models.CASCADE)
    shop_products = models.ForeignKey(ShopProducts, related_name='OrderProducts',verbose_name='Наличие в магазине', on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Количество')
    user = models.ForeignKey(User, related_name='OrderProducts',verbose_name='OrderProducts', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    modified = models.DateTimeField(auto_created=True, auto_now=True)
    price = models.PositiveIntegerField(verbose_name='Цена')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'



