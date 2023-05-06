from tortoise import Model, fields


class Memory(Model):
    key = fields.CharField(pk=True, max_length=32)
    value = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
