from tortoise import Model, fields


class Interaction(Model):
    id = fields.IntField(pk=True)
    prompt = fields.TextField()
    response = fields.TextField()
    session = fields.ForeignKeyField("models.Session", related_name="interactions")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
