import uuid

from django.db.models import (
    Model,
    BooleanField,
    CASCADE,
    CharField,
    ForeignKey,
    PositiveIntegerField,
    SET_NULL,
    UniqueConstraint,
    UUIDField
)

from users.models import Telegram
from stores.models import Product, Store


class Group(Model):
    id = UUIDField(default=uuid.uuid4, primary_key=True)
    admin = ForeignKey(Telegram, on_delete=CASCADE)
    store = ForeignKey(Store, default=None, null=True, on_delete=SET_NULL)
    name = CharField(blank=False, max_length=255)
    collecting = BooleanField(default=False)
    
    def __str__(self) -> str:
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.store:
            self.store = None
            self.collecting = False
        return super().save(*args, **kwargs)


class GroupMember(Model):
    group = ForeignKey(Group, on_delete=CASCADE)
    user = ForeignKey(Telegram, on_delete=CASCADE)


class Cart(Model):
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['group', 'user', 'store', 'product'],
                name='%(app_label)s_%(class)s_relative_uniqueness')
        ]

    group = ForeignKey(Group, on_delete=CASCADE)
    user = ForeignKey(Telegram, on_delete=CASCADE)
    store = ForeignKey(Store, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE)
    amount = PositiveIntegerField()
