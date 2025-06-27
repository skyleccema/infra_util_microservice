from marshmallow import fields as ma_fields, Schema, validate, post_load

from .utils import slot_range_validator
from dataclasses import dataclass
#/query_stb_info

class QueryStbInfoSchemaIn(Schema):
    ip = ma_fields.Str(
        required=True,
        validate=[
            validate.Length(min=7, max=15,
                            error='Ip address must be between 7 and 15 characters')
        ]
    )
    slot = ma_fields.Integer(
        required=True,
        validate=validate.Range(min=1, max=16)#lambda x: slot_range_validator(x)#x>100#lambda x:QueryStbInfoSchema.validate_slot(x)#lambda x: x>100#validate.ValidationError('Slot must be < 3... awwwww',)
    )

@dataclass
class QueryStbInfoOut:
    stb_type: ma_fields.String
    # pin: ma_fields.String
    # ip: ma_fields.String
    # sw_ver: ma_fields.String
    # territory: ma_fields.String
    # server_name: ma_fields.String

class QueryStbInfoDTOOut(Schema):
    stb_type = ma_fields.String(required=True)
    # pin = ma_fields.String(required=True)
    # ip = ma_fields.String(required=True)
    # sw_ver = ma_fields.String(required=True)
    # territory = ma_fields.String(required=True)
    # server_name = ma_fields.String(required=True)

    @post_load
    def getter_result(self, data, **kwargs):
        return QueryStbInfoOut(**data)