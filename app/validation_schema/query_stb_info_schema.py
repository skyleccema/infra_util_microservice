#/query_stb_info
from marshmallow import fields as ma_fields, Schema, validate
from .utils import slot_range_validator, ip_length_validator

class QueryStbInfoSchemaIn(Schema):
    ip = ma_fields.Str(
        required=True,
        validate=lambda x:ip_length_validator(x)#[validate.Length(min=7, max=15, error='Ip address must be between 7 and 15 characters')]
    )
    slot = ma_fields.Integer(
        required=True,
        validate=lambda x: slot_range_validator(x)#validate.Range(min=1, max=16)
    )