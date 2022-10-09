import uuid

from django.db.models import Model, CASCADE, CharField, DecimalField, ForeignKey, JSONField, TextField, UUIDField


class Store(Model):
    class Meta:
        ordering = ['name']

    id = UUIDField(default=uuid.uuid4, primary_key=True)
    address = TextField(blank=False)
    name = CharField(blank=False, max_length=255)

    def __str__(self) -> str:
        return str(self.name)


class Product(Model):
    id = UUIDField(default=uuid.uuid4, primary_key=True)
    store = ForeignKey(Store, on_delete=CASCADE)
    name = CharField(blank=False, max_length=255)
    description = TextField(blank=True)
    # Price for one item bound by million units
    price = DecimalField(max_digits=7, decimal_places=2)
    discount = JSONField(blank=True, default=dict)

    def __str__(self) -> str:
        store = Store.objects.get(id=self.store)
        return f'{store.name} {self.name}'
