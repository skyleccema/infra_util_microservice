from flask_restx import Api, fields, marshal
from flask import Flask
class BoolGenericModel:
    def __init__(self, api: Api, app: Flask):
        self.app = app
        self.api = api

        ### INTEGER HANDLER
        self.bool_model = {
            'Flag': fields.Boolean(required=True)
        }


    def marshal_bool(self, func_output: bool, http_code: int, func_name: str=None) -> tuple[object, int]:
        dao = func_output
        if func_name == "get_stb_status_broken":
            return func_output, http_code
        else:
            model = self.bool_model
            dao = StrDao(func_output)
        self.app.logger.info("Str func_output %s", marshal(data=dao, fields=model))
        return marshal(data=dao, fields=model), http_code


class StrDao(object):
    def __init__(self, my_str):
        self.MyString = my_str