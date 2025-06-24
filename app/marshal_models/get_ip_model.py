from flask_restx import Api, fields, marshal
from flask import Flask
class GetIpModel:
    def __init__(self, api: Api, app: Flask):
        self.app = app
        self.api = api

        #STRING
        self.get_ip_model = {
            'stb_ip': fields.String
        }

    def marshal_str(self, func_output: str, http_code: int) -> tuple[object, int]:
        self.app.logger.info("Str func_output %s\ntype: %s", func_output, type(func_output))
        if func_output == {} or func_output is None:
            raise ValueError(func_output)
        model = self.get_ip_model
        dao = StringGetIpDao(func_output)
        # try:
        #     if func_output == "" or func_output is None:
        #         raise ValueError(func_output)
        # except ValueError as e:
        #     app.logger.info(e)
        #     app.logger.error(format_exc())
        #     func_output = None
        #     http_code = 400
        self.app.logger.info("Type of marshal(data=dao, fields=model)['stb_ip'] %s", type(marshal(data=dao, fields=model)['stb_ip']))
        self.app.logger.info("Str marshal(data=dao, fields=model)['stb_ip'] %s", marshal(data=dao, fields=model)['stb_ip'])
        return marshal(data=dao, fields=model)['stb_ip'], http_code
        # return marshal(data=dao, fields=model), http_code

#STRING
class StringGetIpDao(object):
    def __init__(self, func_output: str):
        self.stb_ip = func_output
