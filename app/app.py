from os import environ, abort
from flask import Flask, make_response, abort
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

load_dotenv('.env', verbose=True)

# import logging, logging.config, yaml
# logging.config.dictConfig(yaml.full_load(open('logging.conf', 'w')))

# logfile    = logging.getLogger('file')
# logconsole = logging.getLogger('console')
# logfile.debug("Debug FILE")
# logconsole.debug("Debug CONSOLE")

import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename="/app/logs/app.log", filemode="w")

# CORS 
CORS(app)
# successivamente accetteremo richieste da subset di IP

def hello():
    return environ.get("ENV")

@app.route("/")
def hello_world():
    # try-except log e tutte le info base su oggetti Flask
    # gestione log Flask con sua libreria ma devo farlo bene
    # nell'except importo la libreria traceback
    # nel log uso la funz di tracecback.formatexec
    # così ho tutto lo stack printato e loggato :)
    try:
        response = hello()
        if response == "development":
            raise ValueError(response)
        result = make_response(hello())
        app.logger.info('LOG_ML: succesfully read and setted ENV')
    except ValueError as e:
        # print_exc()
        # format_exc()
        app.logger.info('LOG_ML: ERROR - %s read ENV', str(e))
        app.logger.error(format_exc())
        result = make_response("None")
        abort(400)
    # result = make_response(hello())
    return result

# missing endpoints
# TBT api_fetch_slots_versions_with_dinamic_filter


# TBD! test fetch_slots_versions_with_dinamic_filter to pick CERRI Slot 16
# problem: cannot guess how to write country code
# tested with http://127.0.0.1:5000/fetch_slots_versions_with_dinamic_filter/CERRI/Llama/ITA/4.0 META3/QS036.018.00U returns empty json
@app.route("/fetch_slots_versions_with_dinamic_filter/<proj>/<platform>/<country>/<rack_name>/<slot_version>")
def api_fetch_slots_versions_with_dinamic_filter(proj, platform, country, rack_name, slot_version):
    return make_response(fetch_slots_versions_with_dinamic_filter(proj, platform, country, rack_name, slot_version))

# tested with http://127.0.0.1:5000/fetch_slots_versions_with_dinamic_filter/CERRI or PCC returns None
@app.route("/fetch_slots_versions_with_dinamic_filter/<proj>")
def api_fetch_slots_versions_with_dinamic_filter_none(proj):
    result = make_response(str(fetch_slots_versions_with_dinamic_filter(proj, None, None, None, None))) 
    return result# result if result is not None else make_response(str(result))

# tested with http://localhost:5000/query_stb_info/10.170.0.199/4
@app.route("/query_stb_info/<ip>/<slot>")
def api_query_stb_info(ip, slot):
    return make_response(str(query_stb_info(ip, slot)))

# tested with http://localhost:5000/get_stb_status_broken/10.170.0.199/4
@app.route("/get_stb_status_broken/<ip>/<slot>")
def api_get_stb_status_broken(ip, slot):
    return make_response(str(get_stb_status_broken(ip, slot)))

# @app.route("/update_broken_status/<ip>/<slot>/<broken>")
# def api_update_broken_status(ip, slot, broken):
#     update_broken_status(ip, slot, broken)

# tested with http://localhost:5000/get_broken_from_rack/10.170.0.199
@app.route("/get_broken_from_rack/<ip_rack>")
def api_get_broken_from_rack(ip_rack):
    return get_broken_from_rack(ip_rack)

@app.route("/query_stb_project_info/<ip>/<slot>")
def api_query_stb_project_info(ip, slot):
    return make_response(query_stb_project_info(ip, slot))

# tested with http://127.0.0.1:5000/get_all_stb
@app.route("/get_all_stb")
def api_get_all_stb():
    return make_response(str(get_all_stb()))

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

# tested with http://127.0.0.1:5000/available_slots/CERRI/Llama
@app.route("/available_slots/<proj>/<typ>")
def api_available_slots(proj, typ):
    return make_response(str(available_slots(proj,typ)))

# tested with http://127.0.0.1:5000/get_auto_reboot
@app.route("/get_auto_reboot")
def api_get_auto_reboot():
    return make_response(str(get_auto_reboot()))

# tested with http://127.0.0.1:5000/get_ip/3/STHD 06/10.170.1.71
@app.route("/get_ip/<slot>/<server>/<ip>")
def api_get_ip(slot, server, ip):
    return get_ip(slot, server, ip)

# tested with http://127.0.0.1:5000/get_stbs_by_project/CERRI
@app.route("/get_stbs_by_project/<proj>")
def api_get_stbs_by_project(proj):
    return make_response(get_stbs_by_project(proj))

# tested with http://127.0.0.1:5000/fetch_slots_versions/CERRI
@app.route("/fetch_slots_versions/<proj>")
def api_fetch_slots_versions(proj):
    return fetch_slots_versions(proj)

# tested with http://127.0.0.1:5000/fetch_rack_slot_type_by_project/PCC but also CERRI
@app.route("/fetch_rack_slot_type_by_project/<proj>")
def api_fetch_rack_slot_type_by_project(proj):
    # INITIALIZE CONNECTION TO DB and FETCH RSL info
    return fetch_rack_slot_type_by_project(proj)


# tested with http://127.0.0.1:5000/fetch_rack_slot_by_project_and_type/CERRI/Llama
@app.route("/fetch_rack_slot_by_project_and_type/<proj>/<typ>")
def api_fetch_rack_slot_by_project_and_type(proj, typ):
    return fetch_rack_slot_by_project_and_type(proj,typ)


# tested with http://127.0.0.1:5000/fetch_rack_slot_type_by_project_grouped_by_rack/PCC but also CERRI
@app.route("/fetch_rack_slot_type_by_project_grouped_by_rack/<proj>")
def api_fetch_rack_slot_type_by_project_grouped_by_rack(proj):
    # INITIALIZE CONNECTION TO DB and FETCH RSL info
    return fetch_rack_slot_type_by_project_grouped_by_rack(proj)

# tested with http://127.0.0.1:5000/fetch_rack_slot_by_project_and_type_grouped_by_rack/CERRI/Llama
@app.route("/fetch_rack_slot_by_project_and_type_grouped_by_rack/<proj>/<typ>")
def api_fetch_rack_slot_by_project_and_type_grouped_by_rack(proj, typ):
    return fetch_rack_slot_by_project_and_type_grouped_by_rack(proj,typ)

