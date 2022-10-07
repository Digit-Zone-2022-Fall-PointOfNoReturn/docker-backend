from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Telegram


class TelegramSerializer(ModelSerializer):
    class Meta:
        model = Telegram
        fields = '__all__'
        read_only_fields = ['id']
