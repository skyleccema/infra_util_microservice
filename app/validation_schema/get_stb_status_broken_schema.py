#/query_stb_info
from marshmallow import fields as ma_fields, Schema, validate
from .utils import project_validator, hw_type_validator, slot_range_validator, ip_length_validator


class GetStbStatusBrokenSchemaIn(Schema):
    ip = ma_fields.String(
        required=True,
        validate=lambda x:ip_length_validator(x)
    )

    slot = ma_fields.Integer(
        required=True,
        validate=lambda x:slot_range_validator(x)
    )