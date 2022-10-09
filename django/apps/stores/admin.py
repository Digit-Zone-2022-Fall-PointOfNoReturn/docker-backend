from django.contrib import admin
from django.http import HttpRequest

from .models import Product, Store


admin.site.register(Product)
admin.site.register(Store)

@admin.register(Product)
class ProductView(admin.ModelAdmin):
    def get_readonly_fields(self, request: HttpRequest, obj: Product = None):
        return [] if obj is None else ['id', 'store']


@admin.register(Store)
class StoreView(admin.ModelAdmin):
    def get_readonly_fields(self, request: HttpRequest, obj: Store = None):
        return [] if obj is None else ['id']
