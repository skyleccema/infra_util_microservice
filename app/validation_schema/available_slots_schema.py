#/query_stb_info
from marshmallow import fields as ma_fields, Schema, validate
from .utils import project_validator, hw_type_validator

class AvailableSlotsSchemaIn(Schema):
    proj = ma_fields.Str(
        required=True,
        validate=lambda x:project_validator(x)
    )

    typ = ma_fields.Str(
        required=True,
        validate=lambda x:hw_type_validator(x)
    )

