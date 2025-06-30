from flask_restx import Api, fields, marshal
from flask import Flask
from dataclasses import dataclass

@dataclass
class QueryStbInfoIn:
    ip: fields.String
    slot: fields.Integer

class QueryStbInfoModel:
    def __init__(self, api: Api, app: Flask):
        self.app = app
        self.api = api

        # self.query_stb_info_model = {
        #     'tuple': fields.List(fields.String)
        # }
        self.query_stb_info_model = {
            'tuple_out': fields.List(fields.String)
            # 'stb_type': fields.String,
            # 'pin': fields.String,
            # 'ip': fields.String,
            # 'sw_ver': fields.String,
            # 'territory': fields.String,
            # 'server_name': fields.String,
        }

    def marshal_tuple(self, func_output: tuple, http_code: int, func_name: str=None) -> tuple[object, int]:
        model = self.query_stb_info_model
        dao = TupleQueryStbInfoDao(func_output)
        if func_output == {} or func_output is None:
            raise ValueError(func_output)
        # try:
        #     if func_output == {} or func_output is None:
        #         raise ValueError(func_output)
        # except ValueError as e:
        #     app.logger.info(e)
        #     app.logger.error(format_exc())
        #     func_output = None
        #     http_code = 400
        self.app.logger.info(func_name)
        return marshal(data=dao, fields=model), http_code

class TupleQueryStbInfoDao(object):
    def __init__(self, tuple_out: tuple):
        self.tuple_out = tuple_out
        # self.stb_type = tuple_out[0]
        # self.pin = tuple_out[1]
        # self.ip = tuple_out[2]
        # self.sw_ver = tuple_out[3]
        # self.territory = tuple_out[4]
        # self.server_name = tuple_out[5]

