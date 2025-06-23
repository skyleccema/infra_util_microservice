from flask_restx import Api, fields, marshal
from flask import Flask
class TupleGenericModel:
    def __init__(self, api: Api, app: Flask):
        self.app = app
        self.api = api

        ### LIST HANDLER
        self.generic_tuple_model = self.api.model('TupleModel', {
            'Tuple': fields.List(cls_or_instance=fields.Raw)
        })

    def marshal_tuple(self, func_output: tuple, http_code: int, func_name: str=None) -> tuple[object, int]:
        model = self.generic_tuple_model
        dao = TupleGenericDao(func_output)
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

class TupleGenericDao(object):
    def __init__(self, mytuple):
        self.Tuple = mytuple
