from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    first_name = models.CharField('имя', max_length=150)
    last_name = models.CharField('фамилия', max_length=150)
    email = models.EmailField('электронная почта', unique=True)
    phone = models.CharField('телефон', max_length=30)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Product(models.Model):
    name = models.CharField('название', max_length=200)
    description = models.TextField('описание')
    price = models.DecimalField('цена', max_digits=10, decimal_places=2)
    image = models.ImageField('изображение', upload_to='products/', blank=True, null=True)
    available = models.BooleanField('в наличии', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self): return self.name
    def get_absolute_url(self): return reverse('product_detail', args=[self.pk])


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('количество', default=1)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'product'], name='one_cart_item_per_product')]

    @property
    def total_price(self): return self.product.price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [('new', 'Новый'), ('paid', 'Оплачен'), ('sent', 'Передан в доставку'), ('done', 'Выполнен')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='orders')
    created_at = models.DateTimeField('создан', auto_now_add=True)
    status = models.CharField('статус', max_length=10, choices=STATUS_CHOICES, default='new')
    total = models.DecimalField('итого', max_digits=12, decimal_places=2, default=Decimal('0'))

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self): return f'Заказ №{self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self): return self.price * self.quantity
