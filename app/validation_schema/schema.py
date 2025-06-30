from marshmallow import fields as ma_fields, Schema, validate, post_load, pre_load

from .utils import slot_range_validator
from dataclasses import dataclass, asdict
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
    # tuple_out: ma_fields.String
    stb_type: ma_fields.String
    pin: ma_fields.String
    ip: ma_fields.String
    sw_ver: ma_fields.String
    territory: ma_fields.String
    server_name: ma_fields.String

class QueryStbInfoDTOOut(Schema):
    # tuple_out = ma_fields.List(ma_fields.String,required=True)
    stb_type = ma_fields.String(required=True)
    pin = ma_fields.String(required=True)
    ip = ma_fields.String(required=True)
    sw_ver = ma_fields.String(required=True)
    territory = ma_fields.String(required=True)
    server_name = ma_fields.String(required=True)

    @pre_load
    def convert_tuple_to_dict(self, data: tuple, **kwargs) -> dict:
        dict_out = {}
        dict_out['stb_type'] = data[0]
        dict_out['pin'] = data[1]
        dict_out['ip'] = data[2]
        dict_out['sw_ver'] = data[3]
        dict_out['territory'] = data[4]
        dict_out['server_name'] = data[5]
        return dict_out

    @post_load
    def getter_result(self, data, **kwargs):
        return QueryStbInfoOut(**data)