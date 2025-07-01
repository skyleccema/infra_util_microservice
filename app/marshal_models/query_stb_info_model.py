#/query_stb_info
from marshmallow import fields as ma_fields, Schema, validate, post_load, pre_load
from dataclasses import dataclass
from ..validation_schema.utils import ip_length_validator


@dataclass
class QueryStbInfoOut:
    # tuple_out: ma_fields.String
    stb_type: ma_fields.String
    pin: ma_fields.String
    ip: ma_fields.String
    sw_ver: ma_fields.String
    territory: ma_fields.String
    server_name: ma_fields.String

class QueryStbInfoDTO(Schema):
    # tuple_out = ma_fields.List(ma_fields.String,required=True)
    stb_type = ma_fields.String(required=True)
    pin = ma_fields.String(required=True)
    ip = ma_fields.String(required=True, validate=lambda x:ip_length_validator(x))
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