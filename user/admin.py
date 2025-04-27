# user/admin.py

from django.contrib import admin
from .models import Profile, Order, OrderItem, Invoice

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__username', 'user__email', 'phone')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('menu_item', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email', 'phone')
    readonly_fields = ('total_amount',)
    inlines = [OrderItemInline]
    list_editable = ('status',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'order', 'invoice_date')
    search_fields = ('invoice_number', 'order__full_name')
    readonly_fields = ('invoice_number', 'order', 'invoice_date')