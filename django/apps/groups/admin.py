from django.contrib import admin

from .models import Cart, Group, GroupMember


admin.site.register(Cart)
admin.site.register(Group)
admin.site.register(GroupMember)
