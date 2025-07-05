from __future__ import annotations

from tortoise import Model, fields
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from autogpt.models.interaction import Interaction


class Session(Model):
    id = fields.IntField(pk=True)
    interaction: fields.ReverseRelation["Interaction"]
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
