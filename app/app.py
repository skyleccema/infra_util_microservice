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

########## marshal classes ########

### DICT HANDLER (or json handler)

#not sure about Nested
dict_model = api.model('DictModel',{
    'dictionary': fields.Nested
})

class DictDao(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary

def marshal_dict(func_output: dict, http_code: int) -> dict:
    return marshal(DictDao(func_output), dict_model), http_code





# TBD! test fetch_slots_versions_with_dinamic_filter to pick CERRI Slot 16
# problem: cannot guess how to write country code
# tested with http://127.0.0.1:5000/fetch_slots_versions_with_dinamic_filter/CERRI/Llama/ITA/4.0 META3/QS036.018.00U returns empty json
@app.route("/fetch_slots_versions_with_dinamic_filter/<proj>/<platform>/<country>/<rack_name>/<slot_version>")
def api_fetch_slots_versions_with_dinamic_filter(proj, platform, country, rack_name, slot_version):
    return make_response(fetch_slots_versions_with_dinamic_filter(proj, platform, country, rack_name, slot_version))

# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/fetch_slots_versions_with_dinamic_filter/<proj>/<platform>/<country>/<rack_name>/<slot_version>")
class FetchSlotsVersionsWithDynamicFilter(Resource):
    def get(self, proj,platform,country,rack_name,slot_version):
        return marshal_dict(fetch_slots_versions_with_dinamic_filter(proj,platform,country,rack_name,slot_version), 200)


# tested with http://127.0.0.1:5000/fetch_slots_versions_with_dinamic_filter/CERRI or PCC returns None
@app.route("/fetch_slots_versions_with_dinamic_filter/<proj>")
def api_fetch_slots_versions_with_dinamic_filter_none(proj):
    result = make_response(str(fetch_slots_versions_with_dinamic_filter(proj, None, None, None, None))) 
    return result# result if result is not None else make_response(str(result))

# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/fetch_slots_versions_with_dinamic_filter/<proj>")
class FetchSlotsVersionsWithDynamicFilterNone(Resource):
    def get(self, proj):
        return marshal_dict(fetch_slots_versions_with_dinamic_filter(proj), 200)

# tested with http://localhost:5000/query_stb_info/10.170.0.199/4
@app.route("/query_stb_info/<ip>/<slot>")
def api_query_stb_info(ip, slot):
    return make_response(str(query_stb_info(ip, slot)))

# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/query_stb_info/<ip>/<slot>")
class QueryStbInfo(Resource):
    def get(self, ip, slot):
        return marshal_dict(query_stb_info/(ip, slot), 200)

# tested with http://localhost:5000/get_stb_status_broken/10.170.0.199/4
@app.route("/get_stb_status_broken/<ip>/<slot>")
def api_get_stb_status_broken(ip, slot):
    return make_response(str(get_stb_status_broken(ip, slot)))

# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/get_stb_status_broken/<ip>/<slot>")
class GetStbStatusBroken(Resource):
    def get(self, ip, slot):
        return marshal_dict(get_stb_status_broken/(ip, slot), 200)

# @app.route("/update_broken_status/<ip>/<slot>/<broken>")
# def api_update_broken_status(ip, slot, broken):
#     update_broken_status(ip, slot, broken)

# tested with http://localhost:5000/get_broken_from_rack/10.170.0.199
@app.route("/get_broken_from_rack/<ip_rack>")
def api_get_broken_from_rack(ip_rack):
    return get_broken_from_rack(ip_rack)

# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/get_broken_from_rack/<ip_rack>")
class GetBrokenFromRack(Resource):
    def get(self, ip_rack):
        return marshal_dict(get_broken_from_rack/(ip_rack), 200)

@app.route("/query_stb_project_info/<ip>/<slot>")
def api_query_stb_project_info(ip, slot):
    return make_response(query_stb_project_info(ip, slot))

# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/query_stb_project_info/<ip>/<slot>")
class QueryStbProjectInfo(Resource):
    def get(self, ip, slot):
        return marshal_dict(query_stb_project_info(ip, slot), 200)

# tested with http://127.0.0.1:5000/get_all_stb
@app.route("/get_all_stb")
def api_get_all_stb():
    return make_response(str(get_all_stb()))

# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/get_all_stb")
class GetAllStb(Resource):
    def get(self):
        return marshal_dict(get_all_stb(), 200)

# tested with http://127.0.0.1:5000/put_stb/?
# ask francesco
# @app.route("/put_stb/<stb>")
# def api_put_stb(stb):
#     return make_response(put_stb(stb))

# tested with http://127.0.0.1:5000/get_rack_slot_by_ip/10.170.0.177
@app.route("/get_rack_slot_by_ip/<ip>")
def api_get_rack_slot_by_ip(ip):
    result = get_rack_slot_by_ip(ip)
    return make_response(result) if result else make_response(str(result))

# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/get_rack_slot_by_ip/<ip>")
class GetRackSlotByIp(Resource):
    def get(self, ip):
        return marshal_dict(get_rack_slot_by_ip(ip), 200)

# tested with http://127.0.0.1:5000/available_slots/CERRI/Llama
@app.route("/available_slots/<proj>/<typ>")
def api_available_slots(proj, typ):
    return make_response(str(available_slots(proj,typ)))

# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/available_slots/<proj>/<typ>")
class AvailableSlot(Resource):
    def get(self, proj, typ):
        return marshal_dict(available_slots(proj, typ), 200)

# tested with http://127.0.0.1:5000/get_auto_reboot
@app.route("/get_auto_reboot")
def api_get_auto_reboot():
    return make_response(str(get_auto_reboot()))

# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/get_auto_reboot")
class GetAutoReboot(Resource):
    def get(self):
        return marshal_dict(get_auto_reboot(), 200)

# tested with http://127.0.0.1:5000/get_ip/3/STHD 06/10.170.1.71
@app.route("/get_ip/<slot>/<server>/<ip>")
def api_get_ip(slot, server, ip):
    return get_ip(slot, server, ip)

# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/get_ip/<slot>/<server>/<ip>")
class GetIp(Resource):
    def get(self, slot, server, ip):
        # fetch_rack_slot_type_by_project(proj), 200
        return marshal_dict(get_ip(slot,server,ip), 200)


# tested with http://127.0.0.1:5000/get_stbs_by_project/CERRI
@app.route("/get_stbs_by_project/<proj>")
def api_get_stbs_by_project(proj):
    return make_response(get_stbs_by_project(proj))

# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/get_stbs_by_project/<proj>")
class GetStbsByProject(Resource):
    def get(self, proj):
        # fetch_rack_slot_type_by_project(proj), 200
        return marshal_dict(get_stbs_by_project(proj), 200)


# tested with http://127.0.0.1:5000/fetch_slots_versions/CERRI
@app.route("/fetch_slots_versions/<proj>")
def api_fetch_slots_versions(proj):
    return fetch_slots_versions(proj)

# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/fetch_slots_versions/<proj>")
class FetchSlotsVersions(Resource):
    def get(self, proj):
        # fetch_rack_slot_type_by_project(proj), 200
        return marshal_dict(fetch_slots_versions(proj), 200)


# tested with http://127.0.0.1:5000/fetch_rack_slot_type_by_project/PCC but also CERRI
@app.route("/fetch_rack_slot_type_by_project/<proj>")
def api_fetch_rack_slot_type_by_project(proj):
    # INITIALIZE CONNECTION TO DB and FETCH RSL info
    return fetch_rack_slot_type_by_project(proj)

# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/fetch_rack_slot_type_by_project/<proj>")
class FetchRackSlotTypeByProject(Resource):
    def get(self, proj):
        # fetch_rack_slot_type_by_project(proj), 200
        return marshal_dict(fetch_rack_slot_type_by_project(proj), 200)


# tested with http://127.0.0.1:5000/fetch_rack_slot_by_project_and_type/CERRI/Llama
@app.route("/fetch_rack_slot_by_project_and_type/<proj>/<typ>")
def api_fetch_rack_slot_by_project_and_type(proj, typ):
    return fetch_rack_slot_by_project_and_type(proj,typ)

# tested with swagger /fetch_rack_slot_by_project_and_type endpoint and proj=PCC, typ=Llama but also CERRI
@api.route("/fetch_rack_slot_by_project_and_type/<proj>/<typ>")
class FetchRackSlotByProjectAndType(Resource):
    def get(self, proj, typ):
        return marshal_dict(fetch_rack_slot_by_project_and_type(proj,typ), 200)

# tested with http://127.0.0.1:5000/fetch_rack_slot_type_by_project_grouped_by_rack/PCC but also CERRI
@app.route("/fetch_rack_slot_type_by_project_grouped_by_rack/<proj>")
def api_fetch_rack_slot_type_by_project_grouped_by_rack(proj):
    # INITIALIZE CONNECTION TO DB and FETCH RSL info
    return fetch_rack_slot_type_by_project_grouped_by_rack(proj)

# tested with swagger /fetch_rack_slot_type_by_project_grouped_by_rack endpoint and proj=PCC but also CERRI
@api.route("/fetch_rack_slot_type_by_project_grouped_by_rack/<proj>")
class FetchRackSlotTypeByProjectGroupedByRack(Resource):
    def get(self, proj):
        return marshal_dict(fetch_rack_slot_type_by_project_grouped_by_rack(proj), 200)


# tested with http://127.0.0.1:5000/fetch_rack_slot_by_project_and_type_grouped_by_rack/CERRI/Llama
@app.route("/fetch_rack_slot_by_project_and_type_grouped_by_rack/<proj>/<typ>")
def api_fetch_rack_slot_by_project_and_type_grouped_by_rack(proj, typ):
    return fetch_rack_slot_by_project_and_type_grouped_by_rack(proj,typ)

# tested with swagger /fetch_rack_slot_by_project_and_type_grouped_by_rack endpoint and proj=PCC, typ=Llama but also CERRI
@api.route("/fetch_rack_slot_by_project_and_type_grouped_by_rack/<proj>/<typ>")
class FetchRackSlotByProjectAndTypeGroupedByRack(Resource):
    def get(self, proj, typ):
        return marshal_dict(fetch_rack_slot_by_project_and_type_grouped_by_rack(proj,typ), 200)

if __name__ == "__main__":
    app.run(debug=True)