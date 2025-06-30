#/available_slots
from marshmallow import fields as ma_fields, Schema, validate, post_load, pre_load
from dataclasses import dataclass
from ..validation_schema.utils import ip_length_validator


@dataclass
class AvailableSlotsOut:
    slots: ma_fields.Integer

class AvailableSlotsDTOOut(Schema):
    slots = ma_fields.Integer(required=True)

    @pre_load
    def out_formatter(self, data, **kwargs):
        return {'slots': data}

    @post_load
    def getter_result(self, data, **kwargs):
        return AvailableSlotsOut(**data)