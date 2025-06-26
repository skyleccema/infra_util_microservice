from flask_restx import Api, fields, marshal, Model
from flask import Flask
from dataclasses import dataclass
from marshmallow import fields as ma_fields

from typing import Any

# @dataclass
# class BoolGeneric:
#     MyBool: bool#fields.Boolean

@dataclass
class GenericGetStbStatusBroken:
    ip: fields.String
    slot: fields.Integer

# def im(api: Api, name: str, **kwargs) -> Model:
# generic model
def im(api: Api, name: str, schema_model: Any) -> Model:
    return  api.model(
        name, schema_model
    )

class BoolGenericModel:
    def __init__(self, api: Api, app: Flask):
        self.app = app
        self.api = api

        self.input_bool_model = api.model(
            'input bool generic model', {
                'ip': fields.String,
                'slot': fields.Integer
            }
        )

        self.bool_model = api.model(
            'input bool generic model', {
                'Flag': fields.Boolean(required=True)
            }
        )


    def marshal_bool(self, func_output: bool, http_code: int, func_name: str=None) -> tuple[object, int]:
        model = self.bool_model#BoolGeneric(func_output)#
        dao = BoolDTO(func_output)#BoolGeneric(func_output)#BoolDTO(func_output)
        self.app.logger.info("Str model %s", model)
        self.app.logger.info("Str dao %s", dao.Flag)
        self.app.logger.info("Str marshal out %s", marshal(data=dao, fields=model))
        return marshal(data=dao, fields=model), http_code

    def get_input_model(self):
        return self.input_bool_model


class BoolDTO(object):
    def __init__(self, my_bool):
        self.Flag = my_bool