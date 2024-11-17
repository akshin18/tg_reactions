from tortoise import fields
from tortoise.models import Model


class Accounts(Model):
    id = fields.BigIntField(pk=True)
    phone = fields.CharField(max_length=255, unique=True)
    pwd = fields.CharField(max_length=255, null=True)
    session_string = fields.TextField()
    is_working = fields.BooleanField(default=True)
    reacted = fields.BigIntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Channels(Model):
    id = fields.BigIntField(pk=True)
    channel_id = fields.BigIntField(unique=True)
    channel_link = fields.CharField(max_length=255)
