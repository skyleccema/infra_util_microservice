#/get_all_stb
from marshmallow import fields as ma_fields, Schema, validate, post_load, pre_load
from dataclasses import dataclass, asdict
from ..validation_schema.utils import ip_length_validator, slot_range_validator
from  flask_restx import fields

@dataclass
class GetAllStbOut:
    __bind_key__: ma_fields.String
    __tablename__: ma_fields.String
    stb_id: ma_fields.Integer(required=True, description="SetTopBox ID")
    slot_id: ma_fields.Integer(description="Slot ID")
    smart_card_id: ma_fields.Integer
    account_id: ma_fields.Integer
    country_code: ma_fields.String
    hardware_name: ma_fields.String
    chipId: ma_fields.String
    deviceid: ma_fields.String
    mac_address_br: ma_fields.String
    model_number: ma_fields.String
    receiverId: ma_fields.String
    project: ma_fields.String
    version_number: ma_fields.String
    serial_number: ma_fields.String
    mac_address: ma_fields.String
    ip: ma_fields.String
    personalized_pin: ma_fields.String
    stb_status: ma_fields.Boolean
    auto_rebot: ma_fields.Boolean
    note: ma_fields.String
    used_for: ma_fields.String
    last_as_status: ma_fields.Boolean
    last_as_date: ma_fields.DateTime
    last_modified: ma_fields.DateTime
    stb_status_info: ma_fields.String
    last_as_call: ma_fields.DateTime

# get_all_stb_output_dict_model =

class GetAllStbDTOOut(Schema):
    __bind_key__ = ma_fields.String
    a__tablename__ = ma_fields.String
    stb_id = ma_fields.Integer(required=True, description="SetTopBox ID")
    slot_id = ma_fields.Integer(description="Slot ID", validate=slot_range_validator)
    smart_card_id = ma_fields.Integer
    account_id = ma_fields.Integer
    country_code = ma_fields.String
    hardware_name = ma_fields.String
    chipId = ma_fields.String
    deviceid = ma_fields.String
    mac_address_br = ma_fields.String
    model_number = ma_fields.String
    receiverId = ma_fields.String
    project = ma_fields.String
    version_number = ma_fields.String
    serial_number = ma_fields.String
    mac_address = ma_fields.String
    ip = ma_fields.String(required=True, validate=lambda x:ip_length_validator(x))
    personalized_pin = ma_fields.String
    stb_status = ma_fields.Boolean
    auto_rebot = ma_fields.Boolean
    note = ma_fields.String
    used_for = ma_fields.String
    last_as_status = ma_fields.Boolean
    last_as_date = ma_fields.DateTime
    last_modified = ma_fields.DateTime
    stb_status_info = ma_fields.String
    last_as_call = ma_fields.DateTime

    @post_load
    def getter_result(self, data, **kwargs):
        return GetAllStbOut(**data)

# from flask_restx import Api, fields, marshal
# from flask import Flask
# class GetAllStbModel:
#     def __init__(self, api: Api, app: Flask):
#         self.app = app
#         self.api = api
#
#         self.list_element_get_all_stb_model = self.api.model(
#             'get_all_stb_model element model', {
#                 '__bind_key__': fields.String,
#                 '__tablename__': fields.String,
#                 'stb_id': fields.Integer(required=True, description='SetTopBox ID'),
#                 'slot_id': fields.Integer(description='Slot ID'),
#                 'smart_card_id': fields.Integer,
#                 'account_id': fields.Integer,
#                 'country_code': fields.String,
#                 'hardware_name': fields.String,
#                 'chipId': fields.String,
#                 'deviceid': fields.String,
#                 'mac_address_br': fields.String,
#                 'model_number': fields.String,
#                 'receiverId': fields.String,
#                 'project': fields.String,
#                 'version_number': fields.String,
#                 'serial_number': fields.String,
#                 'mac_address': fields.String,
#                 'ip': fields.String,
#                 'personalized_pin': fields.String,
#                 'stb_status': fields.Boolean,
#                 'auto_rebot': fields.Boolean,
#                 'note': fields.String,
#                 'used_for': fields.String,
#                 'last_as_status': fields.Boolean,
#                 'last_as_date': fields.DateTime,
#                 'last_modified': fields.DateTime,
#                 'stb_status_info': fields.String,
#                 'last_as_call': fields.DateTime
#             }
#         )
#
#     def marshal_list(self, func_output: list, http_code: int, func_name: str = None) -> tuple[object, int]:
#         self.app.logger.info("Str func_output %s\ntype: %s", func_output, type(func_output))
#         if func_output == {} or func_output is None:
#             raise ValueError(func_output)
#         self.app.logger.info("REPRRR function output:\t%s", func_output)
#         self.app.logger.info("type of output:\t%s", str(type(func_output[0])))
#         model = self.list_element_get_all_stb_model  # self.ref_fields_model#self.list_get_all_stb_model
#         dao = ListElementGetAllStbDao(func_output)
#         # try:
#         #     if func_output == "" or func_output is None:
#         #         raise ValueError(func_output)
#         # except ValueError as e:
#         #     app.logger.info(e)
#         #     app.logger.error(format_exc())
#         #     func_output = None
#         #     http_code = 400
#         self.app.logger.info("Type of marshal(data=dao, fields=model)['stb_ip'] %s", type(marshal(data=dao, fields=model)))
#         self.app.logger.info("Str marshal(data=dao, fields=model)['stb_ip'] %s", marshal(data=dao, fields=model))
#         return marshal(data=dao, fields=model)['stb_ip'], http_code
#         # return marshal(data=dao, fields=model), http_code
#
# #STRING
# class ListElementGetAllStbDao(object):
#     def __init__(self, func_output: list):
#         self.__bind_key__ = func_output[0]
#         self.__tablename__ = func_output[1]
#         self.stb_id = func_output[2]
#         self.slot_id = func_output[3]
#         self.smart_card_id = func_output[4]
#         self.account_id = func_output[5]
#         self.country_code = func_output[6]
#         self.hardware_name = func_output[7]
#         self.chipId = func_output[8]
#         self.deviceid = func_output[9]
#         self.mac_address_br = func_output[10]
#         self.model_number = func_output[11]
#         self.receiverId = func_output[12]
#         self.project = func_output[13]
#         self.version_number = func_output[14]
#         self.serial_number = func_output[13]
#         self.mac_address = func_output[15]
#         self.ip = func_output[16]
#         self.personalized_pin = func_output[17]
#         self.stb_status = func_output[18]
#         self.auto_rebot = func_output[19]
#         self.note = func_output[20]
#         self.used_for = func_output[21]
#         self.last_as_status = func_output[22]
#         self.last_as_date = func_output[23]
#         self.last_modified = func_output[24]
#         self.stb_status_info = func_output[25]
#         self.last_as_call = func_output[26]
