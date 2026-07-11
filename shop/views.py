from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegisterForm
from .models import CartItem, Order, OrderItem, Product


def catalog(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(available=True)
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'shop/catalog.html', {'products': products, 'query': query})


def product_detail(request, pk):
    return render(request, 'shop/product_detail.html', {'product': get_object_or_404(Product, pk=pk, available=True)})


def register(request):
    if request.user.is_authenticated:
        return redirect('catalog')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Добро пожаловать в «Твой орех»!')
        return redirect('catalog')
    return render(request, 'shop/register.html', {'form': form})


@login_required
def add_to_cart(request, product_id):
    if request.method != 'POST': return redirect('product_detail', pk=product_id)
    product = get_object_or_404(Product, pk=product_id, available=True)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created: item.quantity += 1; item.save(update_fields=['quantity'])
    messages.success(request, f'«{product.name}» добавлен в корзину.')
    return redirect(request.POST.get('next') or 'cart')


@login_required
def cart(request):
    items = request.user.cart_items.select_related('product')
    total = sum((item.total_price for item in items), Decimal('0'))
    return render(request, 'shop/cart.html', {'items': items, 'total': total})


@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, user=request.user)
    if request.method == 'POST':
        try: quantity = int(request.POST.get('quantity', 1))
        except ValueError: quantity = 1
        if quantity > 0:
            item.quantity = quantity; item.save(update_fields=['quantity'])
        else: item.delete()
    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST': get_object_or_404(CartItem, pk=item_id, user=request.user).delete()
    return redirect('cart')


@login_required
@transaction.atomic
def checkout(request):
    if request.method != 'POST': return redirect('cart')
    items = list(request.user.cart_items.select_related('product'))
    if not items:
        messages.warning(request, 'Корзина пока пуста.')
        return redirect('cart')
    total = sum((item.total_price for item in items), Decimal('0'))
    order = Order.objects.create(user=request.user, total=total)
    OrderItem.objects.bulk_create([OrderItem(order=order, product_name=i.product.name, price=i.product.price, quantity=i.quantity) for i in items])
    request.user.cart_items.all().delete()
    messages.success(request, f'Заказ №{order.pk} оформлен. Мы свяжемся с вами для оплаты и доставки.')
    return redirect('account')


@login_required
def account(request):
    return render(request, 'shop/account.html', {'orders': request.user.orders.prefetch_related('items')})
