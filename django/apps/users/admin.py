from django.contrib import admin
from django.http.request import HttpRequest

from .models import Telegram


@admin.register(Telegram)
class TelegramView(admin.ModelAdmin):
    def get_readonly_fields(self, request: HttpRequest, obj: Telegram = None):
        return [] if obj is None else ['id']
