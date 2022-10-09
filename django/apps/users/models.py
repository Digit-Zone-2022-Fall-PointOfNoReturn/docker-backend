from django.db.models import Model, PositiveBigIntegerField


class Telegram(Model):
    id = PositiveBigIntegerField(primary_key=True)
