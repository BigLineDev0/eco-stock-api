from django.contrib import admin

from api.models import Product, Warehouse


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity')
    search_fields = ('name', 'location')
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'expiration_date', 'status', 'warehouse')
    list_filter = ('status', 'warehouse')
    search_fields = ('name', 'warehouse__name')
