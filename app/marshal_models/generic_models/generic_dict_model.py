from flask_restx import Api, fields, marshal
from flask import Flask
class DictGenericModel:
    def __init__(self, api: Api, app: Flask):
        self.app = app
        self.api = api

        ### DICT HANDLER (or json handler)
        self.dict_model = self.api.model('DictModel', {
            'dictionary': fields.Raw
        })

    def marshal_dict(self, func_output: dict, http_code: int, func_name: str=None) -> tuple[object, int]:
        model = self.dict_model
        dao = DictDao(func_output)
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

class DictDao(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary
