from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CartItem, Order, OrderItem, Product, User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('Контакты', {'fields': ('phone',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Контакты', {'fields': ('email', 'phone', 'first_name', 'last_name')}),)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available')
    list_filter = ('available',)
    search_fields = ('name', 'description')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'status', 'created_at')
    list_filter = ('status',)
    inlines = [OrderItemInline]

admin.site.register(CartItem)
