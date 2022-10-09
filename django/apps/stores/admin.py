from django.contrib import admin
from django.http import HttpRequest

from .models import Product, Store


@admin.register(Product)
class ProductView(admin.ModelAdmin):
    list_display = ['store_name', 'name']
    
    def get_readonly_fields(self, request: HttpRequest, obj: Product = None):
        return [] if obj is None else ['id', 'store']

    
    def store_name(self, obj: Product) -> str:
        return str(obj.store.name)


@admin.register(Store)
class StoreView(admin.ModelAdmin):
    list_display = ['name']

    def get_readonly_fields(self, request: HttpRequest, obj: Store = None):
        return [] if obj is None else ['id']
