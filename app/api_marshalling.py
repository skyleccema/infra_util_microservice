from flask import Flask
from flask_restx import Api, fields, marshal
from os import environ
from traceback import format_exc

########## marshal classes ########

class MarshallingHandler:
    def __init__(self, api: Api, app: Flask):
        self.api = api
        self.app = app

        ### HELLO HANDLER
        self.model = api.model('Model', {
            'msg': fields.String
        })

        ### DICT HANDLER (or json handler)

        self.dict_model = self.api.model('DictModel', {
            'dictionary': fields.Raw
        })

        ### STRING HANDLER

        self.str_model = self.api.model('StrModel', {
            'MyString': fields.String
        })

        ### INTEGER HANDLER

        self.int_model = {
            'Integer': fields.Integer(required="True")
        }
        # self.int_model = self.api.model('IntegerModel',{
        #     'Integer': fields.Integer(required="True")
        # }))

        ### LIST HANDLER

        self.generic_list_model = self.api.model('ListModel', {
            'List': fields.List(cls_or_instance=fields.Raw)
        })

        self.rack_slot_list_frsbpat = self.api.model('fetch_rack_slot_by_project_and_type element model', {
            'rack_name': fields.String,
            'slot': fields.Integer
        })

        # fetch_rack_slot_by_project_and_type Model
        self.list_frsbpat = self.api.model('fetch_rack_slot_by_project_and_type Model', {
            'List': fields.List(fields.Nested(self.rack_slot_list_frsbpat))
        })

        # CUSTOM FUNCTION HANDLER

        ### TUPLE return

        self.get_rack_slot_by_ip_model = {
            'rack_ip': fields.String,
            'slot_number': fields.Integer
        }

        self.query_stb_info_model = {
            'stb_type': fields.String,
            'pin': fields.String,
            'ip': fields.String,
            'sw_ver': fields.String,
            'territory': fields.String,
            'name': fields.String
        }


    def hello(self):
        return environ.get("ENV")

    def marshal_hello(self, http_code_default):
        return_code = http_code_default
        try:
            response = self.hello()
            if response != "development":
                raise ValueError(response)
            result = response
            self.app.logger.info('LOG_ML: succesfully read and setted %s environment', response)
        except ValueError as e:
            self.app.logger.info('LOG_ML: ERROR - %s unrecognized environment', str(e))
            self.app.logger.error(format_exc())
            result = None
            return_code = 400
        finally:
            return marshal(HelloDao(msg=result), self.model), return_code

    #marshalling methods
    def marshal_dict(self, func_output: dict, http_code: int, func_name: str=None) -> tuple[object, int]:
        if func_name == "get_rack_slot_by_ip":
            model = self.get_rack_slot_by_ip_model
            dao = ToupleGetRackSlotByIpDao(func_output)
        else:
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

    def marshal_tuple(self, func_output: tuple, http_code: int, func_name: str=None) -> tuple[object, int]:
        if func_name == "get_rack_slot_by_ip":
            model = self.get_rack_slot_by_ip_model
            dao = ToupleGetRackSlotByIpDao(func_output)
        else:
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

    def marshal_str(self, func_output: dict, http_code: int) -> tuple[object, int]:
        self.app.logger.info("Str func_output %s\ntype: %s", func_output, type(func_output))
        if func_output == {} or func_output is None:
            raise ValueError(func_output)
        # try:
        #     if func_output == "" or func_output is None:
        #         raise ValueError(func_output)
        # except ValueError as e:
        #     app.logger.info(e)
        #     app.logger.error(format_exc())
        #     func_output = None
        #     http_code = 400
        self.app.logger.info("Str func_output %s", marshal(StrDao(func_output), self.str_model))
        return marshal(data=StrDao(func_output), fields=self.str_model), http_code

    def marshal_int(self, func_output: int, http_code: int, descr: str = None):  # -> tuple[object, int]:
        self.app.logger.info("Int func_output %i\n", func_output)
        if func_output is None:
            http_code = 400
        # try:
        #     if func_output is None:
        #         raise ValueError(func_output)
        # except ValueError as e:
        #     func_output = None
        #     http_code = 400
        self.app.logger.info("marshal Int func_output %s\n", str(marshal(IntegerDao(func_output), self.int_model)))
        return marshal(IntegerDao(func_output), self.int_model), http_code

    def marshal_list(self, func_output: list, http_code: int, func_name: str = None) -> tuple[object, int]:
        self.app.logger.info("List twist and shout func_output %s", str(func_output))
        list_model = self.generic_list_model
        if func_output == () or func_output is None:
            raise ValueError(func_output)
        if func_name is not None:
            list_model = self.list_frsbpat
        # try:
        #     if func_output == () or func_output is None :
        #         raise ValueError(func_output)
        # except ValueError as e:
        #     func_output = None
        #     http_code = 400
        self.app.logger.info("Marshalled List func_output %s", str(marshal(ListDao(func_output), list_model)))
        return marshal(ListDao(func_output), list_model), http_code

class DictDao(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary

class StrDao(object):
    def __init__(self, my_str):
        self.MyString = my_str

class IntegerDao(object):
    def __init__(self, integer):
        self.Integer = integer

class ListDao(object):
    def __init__(self, mylist):
        self.List = mylist

class HelloDao(object):
    def __init__(self, msg):
        self.msg = msg
        # won't be sent in http response
        self.status = 'active'

#Per Function specific class
class ToupleGetRackSlotByIpDao(object):
    def __init__(self, tuple_rack_slot: tuple):
        self.rack_ip = tuple_rack_slot[0]
        self.slot_number = tuple_rack_slot[1]






