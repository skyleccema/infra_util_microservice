from os import environ, abort
from flask import Flask, make_response, abort
from flask_restx import Resource, Api, fields, marshal
from flask_cors import CORS
from traceback import format_exc, print_exc
from infra_utils.QueryInfradb import (query_stb_info,
                                      get_stb_status_broken,
                                      update_broken_status,
                                      get_broken_from_rack,
                                      query_stb_project_info,
                                      get_all_stb,
                                      put_stb,
                                      get_rack_slot_by_ip,
                                      available_slots,
                                      get_auto_reboot,
                                      get_ip,
                                      get_stbs_by_project,
                                      fetch_slots_versions,
                                      fetch_slots_versions_with_dinamic_filter,
                                      fetch_rack_slot_type_by_project,
                                      fetch_rack_slot_by_project_and_type,
                                      fetch_rack_slot_type_by_project_grouped_by_rack,
                                      fetch_rack_slot_by_project_and_type_grouped_by_rack)
from dotenv import load_dotenv
import logging

dotenv_path = '/app/env/.env'
load_dotenv(dotenv_path, verbose=True)

app = Flask(__name__)
api = Api(app)

logging.basicConfig(level=logging.INFO, filename="/app/logs/app.log", filemode="w")

# CORS 
CORS(app)
# successivamente accetteremo richieste da subset di IP

def hello():
    return environ.get("ENV")

model = api.model('Model',{
    'msg': fields.String
})

class HelloDao(object):
    def __init__(self, msg):
        self.msg = msg
        # won't be sent in http response
        self.status = 'active'

def marshal_hello(http_code_default):
    return_code = http_code_default
    try:
        response = hello()
        if response != "development":
            raise ValueError(response)
        result = response
        app.logger.info('LOG_ML: succesfully read and setted %s environment', response)
    except ValueError as e:
        app.logger.info('LOG_ML: ERROR - %s unrecognized environment', str(e))
        app.logger.error(format_exc())
        result = None
        return_code = 400
    finally:
        return marshal(HelloDao(msg=result), model), return_code


@api.route('/hello')
class HelloWorld(Resource):
    # @api.marshal_with(model)
    def get(self):
        return marshal_hello(http_code_default=500)

# missing endpoints
# TBT api_fetch_slots_versions_with_dinamic_filter

# not working properly
# 10.170.1.71

########## marshal classes ########

### DICT HANDLER (or json handler)

dict_model = api.model('DictModel',{
    'dictionary': fields.Raw
})

class DictDao(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary

def marshal_dict(func_output: dict, http_code: int) -> tuple[object, int]:
    try:
        if func_output == {} or func_output is None:
            raise ValueError(func_output)
    except ValueError as e:
        app.logger.info(e)
        app.logger.error(format_exc())
        func_output = None
        http_code = 400
    return marshal(data=DictDao(func_output), fields=dict_model), http_code

### STRING HANDLER

str_model = api.model('StrModel',{
    'str': fields.Raw
})

class StrDao(object):
    def __init__(self, my_str):
        self.my_str = my_str

def marshal_str(func_output: dict, http_code: int) -> tuple[object, int]:
    try:
        if func_output == {} or func_output is None:
            raise ValueError(func_output)
    except ValueError as e:
        app.logger.info(e)
        app.logger.error(format_exc())
        func_output = None
        http_code = 400
    return marshal(data=StrDao(func_output), fields=str_model), http_code


### INTEGER HANDLER
 
int_model = api.model('IntegerModel',{
    'Integer': fields.Integer
})

class IntegerDao(object):
    def __init__(self, integer):
        self.integer = integer

def marshal_int(func_output: int, http_code: int) -> tuple[object, int]:
    try:
        if func_output is None:
            raise ValueError(func_output)
    except ValueError as e:
        func_output = None
        http_code = 400
    return marshal(IntegerDao(func_output), int_model), http_code

### LIST HANDLER

list_model = api.model('ListModel',{
    'List': fields.List
})

class ListDao(object):
    def __init__(self, mylist):
        self.mylist = mylist

def marshal_list(func_output: list, http_code: int) -> tuple[object, int]:
    try:
        if func_output == ():
            raise ValueError(func_output)
    except ValueError as e:
        func_output = None
        http_code = 400
    return marshal(ListDao(func_output), list_model), http_code

# TBD! test fetch_slots_versions_with_dinamic_filter to pick CERRI Slot 16
# problem: cannot guess how to write country code

# test with http://127.0.0.1:5000/fetch_slots_versions_with_dinamic_filter/CERRI/Llama/it/4.0 META3/QS036.018.00U
# tested with http://127.0.0.1:5000/fetch_slots_versions_with_dinamic_filter/CERRI/Llama/ITA/4.0 META3/QS036.018.00U returns empty json
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/fetch_slots_versions_with_dinamic_filter/<proj>/<platform>/<country>/<rack_name>/<slot_version>")
class FetchSlotsVersionsWithDynamicFilter(Resource):
    def get(self,proj,platform,country,rack_name,slot_version):
        return marshal_dict(fetch_slots_versions_with_dinamic_filter(proj,platform,country,rack_name,slot_version), 200)

# tested with http://127.0.0.1:5000/fetch_slots_versions_with_dinamic_filter/CERRI or PCC returns None
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/fetch_slots_versions_with_dinamic_filter/<proj>")
class FetchSlotsVersionsWithDynamicFilterNone(Resource):
    def get(self, proj):
        return marshal_dict(fetch_slots_versions_with_dinamic_filter(proj, None, None, None, None), 200)

# tested with http://localhost:5000/query_stb_info/10.170.0.199/4
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/query_stb_info/<ip>/<slot>")
class QueryStbInfo(Resource):
    def get(self, ip, slot):
        return marshal_dict(query_stb_info/(ip, slot), 200)

# tested with http://localhost:5000/get_stb_status_broken/10.170.0.199/4
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/get_stb_status_broken/<ip>/<slot>")
class GetStbStatusBroken(Resource):
    def get(self, ip, slot):
        return marshal_dict(get_stb_status_broken/(ip, slot), 200)

# # @app.route("/update_broken_status/<ip>/<slot>/<broken>")
# def api_update_broken_status(ip, slot, broken):
#     update_broken_status(ip, slot, broken)

# tested with http://localhost:5000/get_broken_from_rack/10.41.16.113
# tested with swagger /get_broken_from_rack endpoint and ip=10.41.16.113
@api.route("/get_broken_from_rack/<ip_rack>")
class GetBrokenFromRack(Resource):
    def get(self, ip_rack):
        return marshal_dict(get_broken_from_rack/(ip_rack), 200)

# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/query_stb_project_info/<ip>/<slot>")
class QueryStbProjectInfo(Resource):
    def get(self, ip, slot):
        return marshal_dict(str(query_stb_project_info(ip, slot)), 200)

# tested with http://127.0.0.1:5000/get_all_stb
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/get_all_stb")
class GetAllStb(Resource):
    def get(self):
        return marshal_dict(str(get_all_stb()), 200)

# tested with http://127.0.0.1:5000/put_stb/?
# ask francesco
# # @app.route("/put_stb/<stb>")
# def api_put_stb(stb):
#     return make_response(put_stb(stb))

# tested with http://127.0.0.1:5000/get_rack_slot_by_ip/10.170.0.177
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/get_rack_slot_by_ip/<ip>")
class GetRackSlotByIp(Resource):
    def get(self, ip):
        return marshal_dict({ "slot": get_rack_slot_by_ip(ip)}, 200)

# tested with http://127.0.0.1:5000/available_slots/CERRI/Llama
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/available_slots/<proj>/<typ>")
class AvailableSlot(Resource):
    def get(self, proj, typ):
        #understand why marshal_int is now working
        # my_type = str(type(available_slots(proj, typ)))
        # return marshal_str(my_type, 200)
        return marshal_dict(available_slots(proj, typ), 200)

# tested with http://127.0.0.1:5000/get_auto_reboot
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/get_auto_reboot")
class GetAutoReboot(Resource):
    def get(self):
        return marshal_dict(get_auto_reboot(), 200)

# tested with http://127.0.0.1:5000/get_ip/3/STHD 06/10.170.1.71
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/get_ip/<slot>/<server>/<ip>")
class GetIp(Resource):
    def get(self, slot, server, ip):
        # fetch_rack_slot_type_by_project(proj), 200
        return marshal_dict(get_ip(slot,server,ip), 200)


# tested with http://127.0.0.1:5000/get_stbs_by_project/CERRI
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/get_stbs_by_project/<proj>")
class GetStbsByProject(Resource):
    def get(self, proj):
        # fetch_rack_slot_type_by_project(proj), 200
        return marshal_dict(get_stbs_by_project(proj), 200)


# tested with http://127.0.0.1:5000/fetch_slots_versions/CERRI
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/fetch_slots_versions/<proj>")
class FetchSlotsVersions(Resource):
    def get(self, proj):
        # fetch_rack_slot_type_by_project(proj), 200
        return marshal_dict(fetch_slots_versions(proj), 200)


# tested with http://127.0.0.1:5000/fetch_rack_slot_type_by_project/PCC but also CERRI
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/fetch_rack_slot_type_by_project/<proj>")
class FetchRackSlotTypeByProject(Resource):
    def get(self, proj):
        # fetch_rack_slot_type_by_project(proj), 200
        return marshal_dict(fetch_rack_slot_type_by_project(proj), 200)


# tested with http://127.0.0.1:5000/fetch_rack_slot_by_project_and_type/CERRI/Llama
# tested with swagger /fetch_rack_slot_by_project_and_type endpoint and proj=PCC, typ=Llama but also CERRI
@api.route("/fetch_rack_slot_by_project_and_type/<proj>/<typ>")
class FetchRackSlotByProjectAndType(Resource):
    def get(self, proj, typ):
        return marshal_dict(fetch_rack_slot_by_project_and_type(proj,typ), 200)

# tested with http://127.0.0.1:5000/fetch_rack_slot_type_by_project_grouped_by_rack/PCC but also CERRI
# tested with swagger /fetch_rack_slot_type_by_project_grouped_by_rack endpoint and proj=PCC but also CERRI
@api.route("/fetch_rack_slot_type_by_project_grouped_by_rack/<proj>")
class FetchRackSlotTypeByProjectGroupedByRack(Resource):
    def get(self, proj):
        return marshal_dict(fetch_rack_slot_type_by_project_grouped_by_rack(proj), 200)


# tested with http://127.0.0.1:5000/fetch_rack_slot_by_project_and_type_grouped_by_rack/CERRI/Llama
# tested with swagger /fetch_rack_slot_by_project_and_type_grouped_by_rack endpoint and proj=PCC, typ=Llama but also CERRI
@api.route("/fetch_rack_slot_by_project_and_type_grouped_by_rack/<proj>/<typ>")
class FetchRackSlotByProjectAndTypeGroupedByRack(Resource):
    def get(self, proj, typ):
        http_code = 200
        response = fetch_rack_slot_by_project_and_type_grouped_by_rack(proj,typ)
        return marshal_dict(response, http_code)

if __name__ == "__main__":
    app.run(debug=True)