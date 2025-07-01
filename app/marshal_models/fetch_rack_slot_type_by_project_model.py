#/available_slots
from marshmallow import fields as ma_fields, Schema, validate, post_load, pre_load
from dataclasses import dataclass
from ..validation_schema.utils import ip_length_validator
from typing import List


@dataclass
class FetchRackSlotTypeByProjectElementOut:
    rack_name: ma_fields.String
    slot: ma_fields.Integer
    device_type: ma_fields.String

@dataclass
class FetchRackSlotTypeByProjectOut:
    my_list: List[FetchRackSlotTypeByProjectElementOut]

class FetchRackSlotTypeByProjectElementDTO(Schema):
    # slots = ma_fields.Integer(required=True)
    rack_name = ma_fields.String(required=True)
    slot = ma_fields.Integer(required=True)
    device_type = ma_fields.String(required=True)

    # @pre_load
    # def out_formatter(self, data, **kwargs):
    #     return {'slots': data}

    @post_load
    def getter_result(self, data, **kwargs):
        return FetchRackSlotTypeByProjectOut(data).__dict__['my_list']

class FetchRackSlotTypeByProjectDTO(Schema):
    my_list = ma_fields.List(ma_fields.Nested(FetchRackSlotTypeByProjectElementDTO()))
