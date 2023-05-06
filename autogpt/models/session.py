from tortoise import Model, fields


class Session(Model):
    id = fields.IntField(pk=True)
    interaction: fields.ReverseRelation["Interaction"]
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
