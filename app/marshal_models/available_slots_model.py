from flask_restx import Api, fields, marshal
from flask import Flask
from dataclasses import dataclass

@dataclass
class AvailableSlotsIn:
    proj: fields.String
    typ: fields.String

#OLD
class AvailableSlotsModel:
    def __init__(self, api: Api, app: Flask):
        self.app = app
        self.api = api

        #INTEGER
        self.available_slots_model = {
            'available_slots': fields.Integer
        }

    def marshal_int(self, func_output: int, http_code: int) -> tuple[object, int]:  # :
        self.app.logger.info("Int func_output %i\n", func_output)
        if func_output is None:
            http_code = 400
        model = self.available_slots_model
        dao = IntAvailableSlotsDao(func_output)
        self.app.logger.info( "marshal type of marshal(dao, model)['available_slots']) %s\n", type(marshal(dao, model)['available_slots']) ) #marshal(dao, model))
        self.app.logger.info("marshal Int marshal(dao, model)['available_slots']) %i\n", marshal(dao, model)['available_slots']) #marshal(dao, model))
        return marshal(dao, model)['available_slots'], http_code

class IntAvailableSlotsDao(object):
    def __init__(self, func_output: int):
        self.available_slots = func_output