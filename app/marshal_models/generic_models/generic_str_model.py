from flask_restx import Api, fields, marshal
from flask import Flask
class StrGenericModel:
    def __init__(self, api: Api, app: Flask):
        self.app = app
        self.api = api

        ### STRING HANDLER
        self.str_model = self.api.model('StrModel', {
            'MyString': fields.String
        })

    def marshal_str(self, func_output: str, http_code: int, func_name: str=None) -> tuple[object, int]:
        self.app.logger.info("Str func_output %s\ntype: %s", func_output, type(func_output))
        if func_output == {} or func_output is None:
            raise ValueError(func_output)
        model = self.str_model
        dao = StrDao(func_output)
        # try:
        #     if func_output == "" or func_output is None:
        #         raise ValueError(func_output)
        # except ValueError as e:
        #     app.logger.info(e)
        #     app.logger.error(format_exc())
        #     func_output = None
        #     http_code = 400
        self.app.logger.info("Str func_output %s", marshal(data=dao, fields=model))
        return func_output, http_code
        # return marshal(data=dao, fields=model), http_code

class StrDao(object):
    def __init__(self, my_str):
        self.MyString = my_str