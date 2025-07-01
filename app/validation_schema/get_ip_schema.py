#/query_stb_info
from marshmallow import fields as ma_fields, Schema, validate
from .utils import slot_range_validator, ip_length_validator

class GetIpSchemaIn(Schema):
    slot = ma_fields.Int(
        required=True,
        validate=lambda x:slot_range_validator(x)
    )

    server_name = ma_fields.Str(
        required=True
    )

    server_ip = ma_fields.Str(
        required=True,
        validate=lambda x:ip_length_validator(x)
    )
