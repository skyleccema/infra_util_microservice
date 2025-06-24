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
            'tuple': fields.List(fields.Wildcard(fields.String,)),
        }

        # self.query_stb_info_model = {
        #     'stb_type': fields.String,
        #     'pin': fields.String,
        #     'ip': fields.String,
        #     'sw_ver': fields.String,
        #     'territory': fields.String,
        #     'server_name': fields.String
        # }



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

        self.list_element_get_all_stb_model = self.api.model(
            'get_all_stb_model element model', {
                '__bind_key__': fields.String,
                '__tablename__': fields.String,
                'stb_id': fields.Integer(required=True, description='SetTopBox ID'),
                'slot_id': fields.Integer(description='Slot ID'),
                'smart_card_id': fields.Integer,
                'account_id': fields.Integer,
                'country_code': fields.String,
                'hardware_name': fields.String,
                'chipId': fields.String,
                'deviceid': fields.String,
                'mac_address_br': fields.String,
                'model_number': fields.String,
                'receiverId': fields.String,
                'project': fields.String,
                'version_number': fields.String,
                'serial_number': fields.String,
                'mac_address': fields.String,
                'ip': fields.String,
                'personalized_pin': fields.String,
                'stb_status': fields.Boolean,
                'auto_rebot': fields.Boolean,
                'note': fields.String,
                'used_for': fields.String,
                'last_as_status': fields.Boolean,
                'last_as_date': fields.DateTime,
                'last_modified': fields.DateTime,
                'stb_status_info': fields.String,
                'last_as_call': fields.DateTime
            }
        )

        self.ref_fields_model = self.api.model(
            'reference to IAAS stb object', {
                'ref': fields.List(fields.Raw())
                # 'ref': fields.Raw(attribute=lambda x: str(x))
            }
        )

        self.list_get_all_stb_model = self.api.model(
            'get_all_stb list element', {
                # 'ref': fields.List(fields.Raw(attribute=lambda x: str(x)))#(attribute=lambda x: str(x))
                # 'ref': fields.List(fields.Nested(self.ref_fields_model))#(attribute=lambda x: str(x))
                'ref': fields.List(fields.Raw(attribute=lambda x: str(x)))
                # 'obj_id_string': fields.List(InfraDBStbIaasDao)
                # 'obj_id_string': fields.List(fields.Nested(self.list_element_get_all_stb_model))
                # 'obj_id_string': fields.List(fields.String(required=True, description="STB object ID string"),
                #                              description="STBs python object ID string")
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

        # JSON SCHEMA

        address = self.api.schema_model('Address', {
            'properties': {
                'road': {
                    'type': 'string'
                },
            },
            'type': 'object'
        })

        person = self.api.schema_model('Person', {
            'required': ['address'],
            'properties': {
                'name': {
                    'type': 'string'
                },
                'age': {
                    'type': 'integer'
                },
                'birthdate': {
                    'type': 'string',
                    'format': 'date-time'
                },
                'address': {
                    '$ref': '#/definitions/Address',
                }
            },
            'type': 'object'
        })

        address = self.api.schema_model('Address', {
            'properties': {
                'road': {
                    'type': 'string'
                },
            },
            'type': 'object'
        })

        self.query_stb_info_schema = self.api.schema_model('query_stb_info schema', {
            'required': ['address'],
            'properties': {
                "tuple": {
                    "type": "array",
                    "items": [{
                        "type": "string"
                    }, {
                        "type": "string"
                    }, {
                        "type": "string"
                    }, {
                        "type": "string"
                    }, {
                        "type": "string"
                    }, {
                        "type": "string"
                    }, ]
                }
            },
            'type': 'object'
        })

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
            # model = self.query_stb_info_schema
            model = self.query_stb_info_model
            dao = func_output#TupleQueryStbInfoDao(func_output)
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
            # model = self.get_stb_status_broken_model
            # dao = BoolGetIpDao(func_output)
            #return self.app.field.format(func_output), http_code
            # model = PrimitiveField
            # dao = func_output
            return func_output, http_code
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
            self.app.logger.info("type of output:\t%s", str(type(func_output[0])))
            model = self.list_element_get_all_stb_model # self.ref_fields_model#self.list_get_all_stb_model
            dao = func_output#PtrInfraDBStbIaasDao(func_output)
            # envelope="stb_list"
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
        self.app.logger.info( "Marshalled List func_output type %s", type(dao[0]) )
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

class PtrInfraDBStbIaasDao(object):
    def __init__(self, obj_infra_db_stb_iaas: list[InfraDBStbIaas]):
        self.obj_infra_db_stb_iaas = obj_infra_db_stb_iaas


class InfraDBStbIaasDao(fields.Raw):
    def __init__(self, my_object: InfraDBStbIaas):
        super.__init__(super, my_object)
        self.__bind_key__ = my_object.__bind_key__
        self.__tablename__ = my_object.__tablename__
        self.stb_id = my_object.stb_id
        self.slot_id = my_object.slot_id
        self.smart_card_id = my_object.smart_card_id
        self.account_id = my_object.account_id
        self.country_code = my_object.country_code
        self.hardware_name = my_object.hardware_name
        self.chipId = my_object.chipId
        self.deviceid = my_object.deviceid
        self.mac_address_br = my_object.mac_address_br
        self.model_number = my_object.model_number
        self.receiverId = my_object.receiverId
        self.project = my_object.project
        self.version_number = my_object.version_number
        self.serial_number = my_object.serial_number
        self.mac_address = my_object.mac_address
        self.ip = my_object.ip
        self.personalized_pin = my_object.personalized_pin
        self.stb_status = my_object.stb_status
        self.auto_rebot = my_object.auto_rebot
        self.note = my_object.note
        self.used_for = my_object.used_for
        self.last_as_status = my_object.last_as_status
        self.last_as_date = my_object.last_as_date
        self.last_modified = my_object.last_modified
        self.stb_status_info = my_object.stb_status_info
        self.last_as_call = my_object.last_as_call

class StringOrBooleanOrList(fields.Raw):
    __schema_type__ = ["string", "array", "boolean"]
    __schema_example__ = "'hello_word' or ['10.0.1.0/24'] or False"


class PrimitiveField(fields.Raw):
    def format(self, value):
        return value