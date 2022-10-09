from django.http import HttpRequest
from django.contrib import admin

from .models import Cart, Group, GroupMember


@admin.register(Cart)
class CartView(admin.ModelAdmin):
    list_display = ['group', 'user', 'store', 'product', 'amount']

    def get_readonly_fields(self, request: HttpRequest, obj: Cart = None):
        return [] if obj is None else ['group', 'user', 'store', 'product']


@admin.register(Group)
class GroupView(admin.ModelAdmin):
    list_display = ['id']

    def get_readonly_fields(self, request: HttpRequest, obj: Group = None):
        return [] if obj is None else ['id']


@admin.register(GroupMember)
class GroupView(admin.ModelAdmin):
    list_display = ['group', 'user']

    def get_readonly_fields(self, request: HttpRequest, obj: Group = None):
        return [] if obj is None else ['group', 'user']
