from flask_restx import Api, fields, marshal
from flask import Flask
class IntGenericModel:
    def __init__(self, api: Api, app: Flask):
        self.app = app
        self.api = api

        ### INTEGER HANDLER
        self.int_model = {
            'Integer': fields.Integer(required=True)
        }

    def marshal_int(self, func_output: int, http_code: int, func_name: str = None):  # -> tuple[object, int]:
        self.app.logger.info("Int func_output %i\n", func_output)
        if func_output is None:
            http_code = 400
        model = self.int_model
        dao = IntegerDao(func_output)
        # try:
        #     if func_output is None:
        #         raise ValueError(func_output)
        # except ValueError as e:
        #     func_output = None
        #     http_code = 400
        self.app.logger.info("marshal Int func_output %i\n", func_output) #marshal(dao, model))
        return func_output, http_code
        # return marshal(dao, model), http_code

class IntegerDao(object):
    def __init__(self, integer):
        self.Integer = integer