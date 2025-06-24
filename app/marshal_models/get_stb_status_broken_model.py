from flask_restx import Api, fields, marshal
from flask import Flask
class GetStbStatusBrokenModel:
    def __init__(self, api: Api, app: Flask):
        self.app = app
        self.api = api

        #BOOL
        self.get_stb_status_broken_model = {
            'broken': fields.Boolean
        }


    def marshal_bool(self, func_output: bool, http_code: int) -> tuple[object, int]:
        model = self.get_stb_status_broken_model
        dao = BoolGetStbStatusBrokenDao(func_output)
        self.app.logger.info("Type of marshal(data=dao, fields=model)['broken'] %s", type(marshal(data=dao, fields=model)['broken']))
        self.app.logger.info("Str marshal(data=dao, fields=model)['broken'] %s", marshal(data=dao, fields=model)['broken'])
        return marshal(data=dao, fields=model)['broken'], http_code

class BoolGetStbStatusBrokenDao(object):
    def __init__(self, func_output: bool):
        self.broken = func_output