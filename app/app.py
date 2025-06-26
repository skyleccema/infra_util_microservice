
from flask import Flask
from flask_restx import Resource, Api, fields
from flask_cors import CORS
from infra_utils.QueryInfradb import (query_stb_info,
                                      get_stb_status_broken,
                                      get_broken_from_rack,
                                      query_stb_project_info,
                                      get_all_stb,
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
from .marshal_models.api_marshalling import MarshallingHandler
from .marshal_models.generic_models import (DictGenericModel, ListGenericModel,
                            TupleGenericModel, BoolGenericModel, GenericGetStbStatusBroken, im,
                                            IntGenericModel, StrGenericModel)
from .marshal_models import (GetStbStatusBrokenModel, AvailableSlotsModel,
                             GetIpModel, AvailableSlotsCk)

dotenv_path = 'env/.env' # container in /app/ and locally in {HOME}/github_repo
logfile = "logs/app.log" # container in /app/ and locally in {HOME}/github_repo

logging.basicConfig(level=logging.INFO, filename=logfile, filemode="w") #container

load_dotenv(dotenv_path, verbose=True)

app = Flask(__name__)
api = Api(app)
mh=MarshallingHandler(api, app)

#global models
# bool_generic_model = BoolGenericModel(api, app)


# CORS 
CORS(app)
# successivamente accetteremo richieste da subset di IP


@api.route('/hello')
class HelloWorld(Resource):
    # @api.marshal_with(model)
    def get(self):
        return mh.marshal_hello(http_code_default=500)

# missing endpoints
# TBT api_fetch_slots_versions_with_dinamic_filter

# not working properly
# 10.170.1.71

# TBD! test fetch_slots_versions_with_dinamic_filter to pick CERRI Slot 16
# problem: cannot guess how to write country code

# test with http://127.0.0.1:5000/fetch_slots_versions_with_dinamic_filter/CERRI/Llama/it/4.0 META3/QS036.018.00U
# tested with http://127.0.0.1:5000/fetch_slots_versions_with_dinamic_filter/CERRI/Llama/ITA/4.0 META3/QS036.018.00U returns empty list
# library function return list []
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/fetch_slots_versions_with_dinamic_filter/<proj>/<platform>/<country>/<rack_name>/<slot_version>")
class FetchSlotsVersionsWithDynamicFilter(Resource):
    def get(self,proj,platform,country,rack_name,slot_version):
        return mh.marshal_dict(fetch_slots_versions_with_dinamic_filter(proj,platform,country,rack_name,slot_version), 200)

# tested with http://127.0.0.1:5000/fetch_slots_versions_with_dinamic_filter/CERRI or PCC returns None
# library function return list []
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/fetch_slots_versions_with_dinamic_filter/<proj>")
class FetchSlotsVersionsWithDynamicFilterNone(Resource):
    def get(self, proj):
        return mh.marshal_dict(fetch_slots_versions_with_dinamic_filter(proj, None, None, None, None), 200)

# DONE as dictionary
# tested with http://localhost:5000/query_stb_info/10.170.0.199/4
# library function return a tuple ('eu-q-amidala-it', '0000', '10.170.0.210', '6763A3', 'it', 'STHD 07')
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/query_stb_info/<ip>/<slot>")
class QueryStbInfo(Resource):
    def get(self, ip, slot):
        tuple_generic_model = TupleGenericModel(api,app)
        return tuple_generic_model.marshal_tuple(query_stb_info(ip, slot), 200, "query_stb_info")
        # app.logger.debug("type of query_stb_info(ip, slot):\t%s",type(query_stb_info(ip, slot)))
        # app.logger.debug("query_stb_info(ip, slot):\t%s",str(query_stb_info(ip, slot)))
        # return mh.marshal_tuple(query_stb_info(ip, slot), 200, "query_stb_info")

# DONE as dictionary
# tested with http://localhost:5000/get_stb_status_broken/10.170.0.199/4
# library function return a bool False
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/get_stb_status_broken")
class GetStbStatusBroken(Resource):
    @api.expect( im( api,"poc_input_im",
                     {'ip': fields.String, 'slot': fields.Integer} ) )
    def post(self):
        validated_input = GenericGetStbStatusBroken(**api.payload)#BoolGeneric(get_stb_status_broken(ip, slot))
        app.logger.debug("validated_input.ip,validated_input.slot:\t%s\t%i",validated_input.ip,validated_input.slot)
        # get_stb_status_broken_model = GetStbStatusBrokenModel(api,app)
        # return get_stb_status_broken_model.marshal_bool(get_stb_status_broken(ip, slot), 200)
        bool_generic_model = BoolGenericModel(api, app)
        func_output = get_stb_status_broken(validated_input.ip,validated_input.slot)
        app.logger.debug(get_stb_status_broken(validated_input.ip,validated_input.slot))
        return bool_generic_model.marshal_bool(func_output, 200, "get_stb_status_broken")
        # return mh.marshal_bool(get_stb_status_broken(ip, slot), 200, "get_stb_status_broken")


# @api.route("/get_stb_status_broken/<ip>/<slot>")
# class GetStbStatusBroken(Resource):
#     @api.expect(bool_model)
#     def get(self, ip, slot):
#         app.logger.debug(get_stb_status_broken(ip, slot))
#         # get_stb_status_broken_model = GetStbStatusBrokenModel(api,app)
#         # return get_stb_status_broken_model.marshal_bool(get_stb_status_broken(ip, slot), 200)
#         validated_input = BoolGeneric(**api.payload)#BoolGeneric(get_stb_status_broken(ip, slot))
#         bool_generic_model = BoolGenericModel(api,app)
#         func_output = get_stb_status_broken(validated_input.ip,validated_input.slot)
#         return bool_generic_model.marshal_bool(func_output, 200, "get_stb_status_broken")
#         # return mh.marshal_bool(get_stb_status_broken(ip, slot), 200, "get_stb_status_broken")


# # @app.route("/update_broken_status/<ip>/<slot>/<broken>")
# def api_update_broken_status(ip, slot, broken):
#     update_broken_status(ip, slot, broken)

# DONE (to be tested with IP of a rack with broken devices... by now are None for this IP)
# tested with http://localhost:5000/get_broken_from_rack/10.41.16.113
# library function return a dictionary {'rack_ip': '10.41.16.113', 'slots': [13]}
# tested with swagger /get_broken_from_rack endpoint and ip=10.41.16.113
@api.route("/get_broken_from_rack/<ip_rack>")
class GetBrokenFromRack(Resource):
    def get(self, ip_rack):
        app.logger.info("get_broken_from_rack(ip_rack) f output:\t%s", str(get_broken_from_rack(ip_rack)))
        return mh.marshal_dict(get_broken_from_rack(ip_rack), 200, "get_broken_from_rack")

# DONE as dictionary
# tested with http://localhost:5000/query_stb_info/10.170.0.199/4
# library function return a tuple ('eu-q-amidala-it', '0000', '10.170.0.210', '6763A3', 'it', 'STHD 07', 'PCC')
# tested with swagger /fetch_rack_slot_type_by_project endpoint and ip=10.170.0.199 slot=4
@api.route("/query_stb_project_info/<ip>/<slot>")
class QueryStbProjectInfo(Resource):
    def get(self, ip, slot):
        return mh.marshal_tuple(query_stb_project_info(ip, slot), 200,"query_stb_project_info")

# TBD
# tested with http://127.0.0.1:5000/get_all_stb
# library function return a list [<infra_utils.models.infradb_Iaas.InfraDBStbIaas object at 0x72892c7256a0>, \
# <infra_utils.models.infradb_Iaas.InfraDBStbIaas object at 0x72892c6c4cd0>, ... ]
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/get_all_stb")
class GetAllStb(Resource):
    def get(self):
        return mh.marshal_list(get_all_stb(), 200, "get_all_stb")
        # return mh.marshal_dict(get_all_stb(), 200, "get_all_stb")

# tested with http://127.0.0.1:5000/put_stb/?
# ask francesco
# # @app.route("/put_stb/<stb>")
# def api_put_stb(stb):
#     return make_response(put_stb(stb))

# TBD (output should be identical to input)
# tested with http://127.0.0.1:5000/get_rack_slot_by_ip/10.170.0.177
# library function return a tuple "10.170.0.167", 3
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/get_rack_slot_by_ip/<ip>")
class GetRackSlotByIp(Resource):
    def get(self, ip):
        app.logger.info(type(get_rack_slot_by_ip(ip)))
        return mh.marshal_tuple(get_rack_slot_by_ip(ip), 200, "get_rack_slot_by_ip")

# DONE
# tested with http://127.0.0.1:5000/available_slots/CERRI/Llama
# library function return a int 2
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
# @api.route("/available_slots/<proj>/<typ>")
@api.route("/available_slots")
class AvailableSlots(Resource):
    @api.expect(im(api,'available slot schema',
                {'proj': fields.String, 'typ': fields.String}))
    def post(self):
        #understand why marshal_int is now working
        # my_type = str(type(available_slots(proj, typ)))
        # return marshal_str(my_type, 200)
        # int_generic_model = IntGenericModel(api, app)
        # return int_generic_model.marshal_int(available_slots(proj, typ), 200, "available_slots")
        # return int.marshal_int(available_slots(proj, typ), 200, "available_slots")
        validated_input = AvailableSlotsCk(**api.payload)
        app.logger.debug('validated_inputs\t%s\t%s',validated_input.proj, validated_input.typ)
        available_slots_model = AvailableSlotsModel(api,app)
        return available_slots_model.marshal_int(
            available_slots(validated_input.proj, validated_input.typ),
            200
        )
        #OLD WORKING
        # available_slots_model = AvailableSlotsModel(api,app)
        # return available_slots_model.marshal_int(available_slots(proj,typ), 200)

# DONE
# tested with http://127.0.0.1:5000/get_auto_reboot
# library function return a list [{'slot': 3, 'magiq': '10.170.0.39'}, {'slot': 4, 'magiq': '10.170.0.39'}, ...]
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/get_auto_reboot")
class GetAutoReboot(Resource):
    def get(self):
        return mh.marshal_list(get_auto_reboot(), 200, "get_auto_reboot")

# DONE
# tested with http://127.0.0.1:5000/get_ip/3/STHD 06/10.170.1.71
# library function return a string '10.170.0.177'
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/get_ip/<slot>/<server>/<ip>")
class GetIp(Resource):
    def get(self, slot, server, ip):
        # fetch_rack_slot_type_by_project(proj), 200
        app.logger.info("get_ip(slot,server,ip) type: %s",type(get_ip(slot,server,ip)))
        get_ip_model = GetIpModel(api,app)
        return get_ip_model.marshal_str(str(get_ip(slot,server,ip)), 200)
        # str_generic_model = StrGenericModel(api,app)
        # return str_generic_model.marshal_str(get_ip(slot,server,ip), 200, "get_ip")
        # return mh.marshal_str(str(get_ip(slot,server,ip)), 200, "get_ip")


# DONE
# tested with http://127.0.0.1:5000/get_stbs_by_project/CERRI
# library function return a list [{'rack_ip': '10.170.1.71', 'slot': 3}, {'rack_ip': '10.170.1.71', 'slot': 8} ...]
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/get_stbs_by_project/<proj>")
class GetStbsByProject(Resource):
    def get(self, proj):
        # fetch_rack_slot_type_by_project(proj), 200
        return mh.marshal_list(get_stbs_by_project(proj), 200, 'get_stbs_by_project')


# DONE
# tested with http://127.0.0.1:5000/fetch_slots_versions/CERRI
# library function return a list [{'rack_ip': '10.170.1.71', 'slot': 3, 'version': 'Q310.000.08.00D'}, {'rack_ip': '10.170.1.71', 'slot': 8, 'version': 'Q270.000.09.00D'}, ...]
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/fetch_slots_versions/<proj>")
class FetchSlotsVersions(Resource):
    def get(self, proj):
        # fetch_rack_slot_type_by_project(proj), 200
        return mh.marshal_list(fetch_slots_versions(proj), 200, 'fetch_slots_versions')


# DONE
# tested with http://127.0.0.1:5000/fetch_rack_slot_type_by_project/PCC but also CERRI
# library function return a list [{'rack_name': '4.0 META3', 'slot': 3, 'device_type': 'Falcon'}, ...]
# tested with swagger /fetch_rack_slot_type_by_project endpoint and proj=PCC but also CERRI
@api.route("/fetch_rack_slot_type_by_project/<proj>")
class FetchRackSlotTypeByProject(Resource):
    def get(self, proj):
        # DictionaryGenericModel = DictGenericModel(api, app)
        # return DictionaryGenericModel.marshal_dict(fetch_rack_slot_type_by_project(proj), 200, "fetch_rack_slot_type_by_project")
        return mh.marshal_list(fetch_rack_slot_type_by_project(proj), 200, "fetch_rack_slot_type_by_project")
        # return mh.marshal_list(fetch_rack_slot_type_by_project(proj), 200, "fetch_rack_slot_type_by_project")


# DONE
# tested with http://127.0.0.1:5000/fetch_rack_slot_by_project_and_type/CERRI/Llama
# library function return a list [{'rack_name': '4.0 META3', 'slot': 12}, {'rack_name': '4.0 META3', 'slot': 16}]
# tested with swagger /fetch_rack_slot_by_project_and_type endpoint and proj=PCC, typ=Llama but also CERRI
@api.route("/fetch_rack_slot_by_project_and_type/<proj>/<typ>")
class FetchRackSlotByProjectAndType(Resource):
    def get(self, proj, typ):
        list_generic_model = ListGenericModel(api, app)
        return list_generic_model.marshal_list(fetch_rack_slot_by_project_and_type(proj,typ), 200, "fetch_rack_slot_by_project_and_type")
        # return mh.marshal_list(fetch_rack_slot_by_project_and_type(proj,typ), 200, "fetch_rack_slot_by_project_and_type")

# DONE
# tested with http://127.0.0.1:5000/fetch_rack_slot_type_by_project_grouped_by_rack/PCC but also CERRI
# library function return a dictionary
# {'records': [{'rack_name': '4.0 META3', 'devices': [{'slot': 3, 'device_type': 'Falcon'}, \
# {'slot': 8, 'device_type': 'Amidala'}, {'slot': 9, 'device_type': 'Titan'}, \
# {'slot': 10, 'device_type': 'MRBOX'}, {'slot': 11, 'device_type': 'Stream'}, \
# {'slot': 12, 'device_type': 'Llama'}, {'slot': 16, 'device_type': 'Llama'}, \
# {'slot': 6, 'device_type': 'MySkyHD'}, {'slot': 7, 'device_type': 'Amidala_Hip'}]}]}
# tested with swagger /fetch_rack_slot_type_by_project_grouped_by_rack endpoint and proj=PCC but also CERRI
@api.route("/fetch_rack_slot_type_by_project_grouped_by_rack/<proj>")
class FetchRackSlotTypeByProjectGroupedByRack(Resource):
    def get(self, proj):
        return mh.marshal_dict(fetch_rack_slot_type_by_project_grouped_by_rack(proj), 200, "fetch_rack_slot_type_by_project_grouped_by_rack")


# DONE
# tested with http://127.0.0.1:5000/fetch_rack_slot_by_project_and_type_grouped_by_rack/CERRI/Llama
# library function return a dictionary {'records': [{'rack_name': '4.0 META3', 'devices': [{'slot': 12}, {'slot': 16}]}]}
# tested with swagger /fetch_rack_slot_by_project_and_type_grouped_by_rack endpoint and proj=PCC, typ=Llama but also CERRI
@api.route("/fetch_rack_slot_by_project_and_type_grouped_by_rack/<proj>/<typ>")
class FetchRackSlotByProjectAndTypeGroupedByRack(Resource):
    def get(self, proj, typ):
        return mh.marshal_dict(func_output = fetch_rack_slot_by_project_and_type_grouped_by_rack(proj,typ),
                               http_code = 200,
                               func_name = "fetch_rack_slot_by_project_and_type_grouped_by_rack")

if __name__ == "__main__":
    app.run(debug=True)