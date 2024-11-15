from tortoise import fields
from tortoise.models import Model


class Accounts(Model):
    id = fields.BigIntField(pk=True)
