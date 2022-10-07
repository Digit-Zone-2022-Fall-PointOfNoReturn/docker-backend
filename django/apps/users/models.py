import uuid

from django.db.models import Model, UUIDField, CharField


class Telegram(Model):
    id = UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    # Some users have no tag (but it must be unique if set)
    tag = CharField(blank=True, unique=True, max_length=255)
    # Any user have name. That field required if we want to have
    #   an ability to find someone without tag
    name = CharField(blank=False, max_length=255)
