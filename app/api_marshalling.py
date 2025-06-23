from flask import Flask
from flask_restx import Api, fields, marshal
from os import environ
from traceback import format_exc
from infra_utils.QueryInfradb import InfraDBStbIaas
from datetime import datetime

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

        ### LIST HANDLER

        self.generic_list_model = self.api.model('ListModel', {
            'List': fields.List(cls_or_instance=fields.Raw)
        })


        # CUSTOM FUNCTION HANDLER

        ### TUPLE return

        self.get_rack_slot_by_ip_model = self.api.model(
            "Tuple", {
                'rack_ip': fields.String,
                'slot_number': fields.Integer
            }
        )

        self.query_stb_info_model = {
            'stb_type': fields.String,
            'pin': fields.String,
            'ip': fields.String,
            'sw_ver': fields.String,
            'territory': fields.String,
            'server_name': fields.String
        }

        self.query_stb_project_info_model = {
            'stb_type': fields.String,
            'pin': fields.String,
            'ip': fields.String,
            'sw_ver': fields.String,
            'territory': fields.String,
            'server_name': fields.String,
            'project': fields.String
        }

        #INTEGER
        self.available_slots_model = {
            'available_slots': fields.Integer
        }

        #STRING
        self.get_ip_model = {
            'stb_ip': fields.String
        }

        #BOOL
        self.get_stb_status_broken_model = {
            'broken': fields.Boolean
        }

        #LIST
        ### fetch_rack_slot_by_project_and_type
        self.list_element_fetch_rack_slot_by_project_and_type_model = self.api.model(
            'fetch_rack_slot_by_project_and_type_model element model', {
                'rack_name': fields.String(required=True, description='The rack name'),
                'slot': fields.Integer(required=True, description='Slot number')
            }
        )

        ### fetch_rack_slot_type_by_project
        self.list_element_fetch_rack_slot_type_by_project_model = self.api.model(
            'fetch_rack_slot_by_project_and_type_model element model', {
                'rack_name': fields.String(required=True, description='The rack name'),
                'slot': fields.Integer(required=True, description='Slot number'),
                'device_type': fields.String(description='Device type')
            }
        )

        self.list_fetch_slots_versions_model = self.api.model(
            'list_fetch_slots_versions_model element model', {
                'rack_ip': fields.String(required=True, description='Rack Ip'),
                'slot': fields.Integer(required=True, description='Slot Number'),
                'version': fields.String(description='Slot Model Version')
            }
        )

        self.list_get_stbs_by_project_model = self.api.model(
            'get_stbs_by_project element model', {
                'rack_ip': fields.String(required=True, description='Rack Ip'),
                'slot': fields.Integer(required=True, description='Slot Number')
            }
        )

        self.list_get_auto_reboot_model = self.api.model(
            'get_auto_reboot element model',{
                'slot': fields.Integer(required=True, description='Slot Number'),
                'magiq': fields.String(required=True, description='MagicQ Ip')
            }
        )

        self.list_get_all_stb_model = self.api.model(
            'get_all_stb list element', {
                'obj_id_string': fields.List(fields.String(required=True, description="STB object ID string"),
                                     description="STBs python object ID string")
            }
        )

        #DICT

        ### fetch_rack_slot_by_project_and_type_grouped_by_rack
        self.slot_model = {
            'slot': fields.Integer(required=True, description='Slot number')
        }

        self.list_element_fetch_rack_slot_by_project_and_type_grouped_by_rack_model = self.api.model(
            'fetch_rack_slot_by_project_and_type_grouped_by_rack element model', {
                'rack_name': fields.String(required=True, description='The rack name'),
                'devices': fields.List(fields.Nested(self.slot_model), description='slots')
            }
        )

        self.dict_fetch_rack_slot_by_project_and_type_grouped_by_rack_model = self.api.model(
            'fetch_rack_slot_by_project_and_type_grouped_by_rack element model', {
                'records': fields.List(
                    fields.Nested(
                        self.list_element_fetch_rack_slot_by_project_and_type_grouped_by_rack_model,
                        description="List of racks"
                    )
                )
            }
        )

        ### fetch_rack_slot_type_by_project_grouped_by_rack
        self.slot_type_model = self.api.model(
            "slot and type sub-element model", {
            'slot': fields.Integer(required=True, description='Slot number'),
            'device_type': fields.String(required=True, description='Slot number')
        })

        self.list_element_fetch_rack_slot_type_by_project_grouped_by_rack_model = self.api.model(
            'fetch_rack_slot_by_project_and_type_grouped_by_rack element model', {
                'rack_name': fields.String(required=True, description='The rack name'),
                'devices': fields.List(fields.Nested(self.slot_type_model), description='slots')
            }
        )

        self.dict_fetch_rack_slot_type_by_project_grouped_by_rack_model = self.api.model(
            'fetch_rack_slot_by_project_and_type_grouped_by_rack element model', {
                'records': fields.List(
                    fields.Nested(
                        self.list_element_fetch_rack_slot_type_by_project_grouped_by_rack_model,
                        description="List of racks"
                    )
                )
            }
        )
        self.dict_get_broken_from_rack_model = self.api.model(
            'get_broken_from_rack dictionary', {
                'json_broken': fields.Raw
                # 'rack_ip': fields.String(required=True, description="Rack IP address"),
                # 'slots': fields.List(InfraDBStbIaas(),
                #                      description="Slot number")
                # 'slots': fields.Integer(required=True, description="Rack IP address")
            }
        )

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
        dao = func_output
        if func_name == "fetch_rack_slot_by_project_and_type_grouped_by_rack":
            model = self.dict_fetch_rack_slot_by_project_and_type_grouped_by_rack_model
        elif func_name == "fetch_rack_slot_type_by_project_grouped_by_rack":
            self.app.logger.info("function output:\t%s", str(func_output))
            model = self.dict_fetch_rack_slot_type_by_project_grouped_by_rack_model
        elif func_name == "get_broken_from_rack":
            self.app.logger.info("function output:\t%s", str(func_output))
            model = self.dict_get_broken_from_rack_model
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
        if func_output == {} or func_output is None:
            raise ValueError(func_output)
        if func_name == "get_rack_slot_by_ip":
            model = self.get_rack_slot_by_ip_model
            dao = TupleGetRackSlotByIpDao(func_output)
        elif func_name == "query_stb_info":
            model = self.query_stb_info_model
            dao = TupleQueryStbInfoDao(func_output)
        elif func_name == "query_stb_project_info":
            model = self.query_stb_project_info_model
            dao = TupleQueryStbProjectInfoDao(func_output)
        else:
            model = self.dict_model
            dao = DictDao(func_output)
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

    def marshal_str(self, func_output: str, http_code: int, func_name: str=None) -> tuple[object, int]:
        self.app.logger.info("Str func_output %s\ntype: %s", func_output, type(func_output))
        if func_output == {} or func_output is None:
            raise ValueError(func_output)
        if func_name == "get_ip":
            model = self.get_ip_model
            dao = StringGetIpDao(func_output)
        else:
            model = self.int_model
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
        return marshal(data=dao, fields=model), http_code

    def marshal_bool(self, func_output: bool, http_code: int, func_name: str=None) -> tuple[object, int]:
        self.app.logger.info("Str func_output %s\ntype: %s", func_output, type(func_output))
        dao = func_output
        if func_output == {} or func_output is None:
            raise ValueError(func_output)
        if func_name == "get_stb_status_broken":
            model = self.get_stb_status_broken_model
            dao = BoolGetIpDao(func_output)
        else:
            model = self.int_model
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
        return marshal(data=dao, fields=model), http_code

    def marshal_int(self, func_output: int, http_code: int, func_name: str = None):  # -> tuple[object, int]:
        self.app.logger.info("Int func_output %i\n", func_output)
        if func_output is None:
            http_code = 400
        if func_name == "available_slots":
            model = self.available_slots_model
            dao = IntAvailableSlotsDao(func_output)
        else:
            model = self.int_model
            dao = IntegerDao(func_output)
        # try:
        #     if func_output is None:
        #         raise ValueError(func_output)
        # except ValueError as e:
        #     func_output = None
        #     http_code = 400
        self.app.logger.info("marshal Int func_output %i\n", func_output) #marshal(dao, model))
        return marshal(dao, model), http_code

    def marshal_list(self, func_output: list, http_code: int, func_name: str = None) -> tuple[object, int]:
        self.app.logger.info("marshal_list: func_output %s", str(func_output))
        envelope = None
        dao = func_output
        if func_output == () or func_output is None:
            raise ValueError(func_output)
        if func_name == "fetch_rack_slot_type_by_project":
            self.app.logger.info("marshal_list - dentro if fetch_rack_slot_type_by_project\t%s",func_output)
            model = self.list_element_fetch_rack_slot_type_by_project_model
        elif func_name == "fetch_rack_slot_by_project_and_type":
            self.app.logger.info("WEEEEEEEEE")
            model = self.list_element_fetch_rack_slot_by_project_and_type_model
        elif func_name == "fetch_rack_slot_by_project_and_type_grouped_by_rack":
            self.app.logger.info("function output:\t%s", str(func_output))
            model = self.list_element_fetch_rack_slot_by_project_and_type_grouped_by_rack_model
        elif func_name == "fetch_slots_versions":
            self.app.logger.info("function output:\t%s", str(func_output))
            model = self.list_fetch_slots_versions_model
        elif func_name == "get_stbs_by_project":
            self.app.logger.info("function output:\t%s", str(func_output))
            model = self.list_get_stbs_by_project_model
        elif func_name == "get_auto_reboot":
            self.app.logger.info("function output:\t%s", str(func_output))
            model = self.list_get_auto_reboot_model
        elif func_name == "get_all_stb":
            self.app.logger.info("function output:\t%s", str(func_output))
            model = self.list_get_all_stb_model
        else:
            model = self.generic_list_model
            dao = ListGenericDao(func_output)
        # try:
        #     if func_output == () or func_output is None :
        #         raise ValueError(func_output)
        # except ValueError as e:
        #     func_output = None
        #     http_code = 400
        self.app.logger.info( "Marshalled List func_output %s", marshal(dao, model) )
        # return marshal(dao, fields.List(model)), http_code
        return marshal(dao, model, envelope=envelope), http_code

class DictDao(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary

class StrDao(object):
    def __init__(self, my_str):
        self.MyString = my_str

class IntegerDao(object):
    def __init__(self, integer):
        self.Integer = integer

class ListGenericDao(object):
    def __init__(self, mylist):
        self.List = mylist

class HelloDao(object):
    def __init__(self, msg):
        self.msg = msg
        # won't be sent in http response
        self.status = 'active'

#Per Function specific class
#TUPLES
class TupleGetRackSlotByIpDao(object):
    def __init__(self, tuple_out: tuple):
        self.rack_ip = tuple_out[0]
        self.slot_number = tuple_out[1]

class TupleQueryStbInfoDao(object):
    def __init__(self, tuple_out: tuple):
        self.stb_type = tuple_out[0]
        self.pin = tuple_out[1]
        self.ip = tuple_out[2]
        self.sw_ver = tuple_out[3]
        self.territory = tuple_out[4]
        self.server_name = tuple_out[5]

class TupleQueryStbProjectInfoDao(TupleQueryStbInfoDao):
    def __init__(self, tuple_out: tuple):
        super().__init__(tuple_out)
        self.project = tuple_out[6]

#INTEGER
class IntAvailableSlotsDao(object):
    def __init__(self, func_output: int):
        self.available_slots = func_output

#STRING
class StringGetIpDao(object):
    def __init__(self, func_output: str):
        self.stb_ip = func_output

#STRING
class BoolGetIpDao(object):
    def __init__(self, func_output: bool):
        self.broken = func_output

#LIST
class ListFetchRackSlotByProjectAndTypeDao(object):
    def __init__(self, func_output: list[dict]):
        self.RackSlots = func_output

class ListFetchRackSlotByProjectAndTypeGroupedByRackDao(object):
    def __init__(self, func_output: list[dict]):
        self.rack_and_slot = func_output

#DICT

class ListElementFetchRackSlotByProjectAndTypeDao(object):
    def __init__(self, rack_name: str, slot: int):
        self.rack_name = rack_name
        self.slot = slot

class GroupedByRackDao(object):
    def __init__(self, my_dict: dict):
        self.records = my_dict

class SlotsDao(object):
    def __init__(self, slot: int):
        self.slot = slot

# class DictFetchRackSlotTypeByProjectGroupedByRackDao(object):
#     def __init__(self, records: dict):
#         self.records = records

# class InfraDBStbIaasDao():
#     def __init__(self, stb_id: int, slot_id: int, smart_card_id: int, account_id: int,
#                  country_code: str, hardware_name: str, chip_id: str, deviceid: str,
#                  mac_address_br: str, model_number: str, receiver_id: str, project: str,
#                  version_number: str, serial_number: str, mac_address: str, ip: str,
#                  personalized_pin: str, stb_status: str, auto_rebot: str, note: str,
#                  used_for: str, last_as_status: bool, last_as_date: datetime,
#                  last_modified: datetime, stb_status_info: str, last_as_call: datetime):
#         super.__init__(self)
#         self.__bind_key__ = 'infradb'
#         self.__tablename__ = 'stb_iaas'
#         self.stb_id = stb_id
#         self.slot_id = slot_id
#         self.smart_card_id = smart_card_id
#         self.account_id = account_id
#         self.country_code = country_code
#         self.hardware_name = hardware_name
#         self.chipId = chip_id
#         self.deviceid = deviceid
#         self.mac_address_br = mac_address_br
#         self.model_number = model_number
#         self.receiverId = receiver_id
#         self.project = project
#         self.version_number = version_number
#         self.serial_number = serial_number
#         self.mac_address = mac_address
#         self.ip = ip
#         self.personalized_pin = personalized_pin
#         self.stb_status = stb_status
#         self.auto_rebot = auto_rebot
#         self.note = note
#         self.used_for = used_for
#         self.last_as_status = last_as_status
#         self.last_as_date = last_as_date
#         self.last_modified = last_modified
#         self.stb_status_info = stb_status_info
#         self.last_as_call = last_as_call
