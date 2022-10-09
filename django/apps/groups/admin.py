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
    list_display = ['id', 'name']

    def get_form(self, request: HttpRequest, obj: Group = None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['store'].required = False
        return form

    def get_readonly_fields(self, request: HttpRequest, obj: Group = None):
        return [] if obj is None else ['id']


@admin.register(GroupMember)
class GroupMemberView(admin.ModelAdmin):
    list_display = ['group', 'user']

    def get_readonly_fields(self, request: HttpRequest, obj: Group = None):
        return [] if obj is None else ['group', 'user']
