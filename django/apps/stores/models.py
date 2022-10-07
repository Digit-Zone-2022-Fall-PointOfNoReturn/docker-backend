import uuid

from django.db.models import Model, CASCADE, CharField, DecimalField, ForeignKey, JSONField, TextField, UUIDField


class Store(Model):
    class Meta:
        ordering = ['name']

    id = UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    address = TextField(blank=False)
    name = CharField(blank=False, max_length=255)


class Product(Model):
    class Meta:
        ordering = ['name']
    
    id = UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    store = ForeignKey(Store, on_delete=CASCADE)
    name = CharField(blank=False, max_length=255)
    description = TextField(blank=True)
    price = DecimalField(decimal_places=2)
    discount = JSONField(default=dict)
