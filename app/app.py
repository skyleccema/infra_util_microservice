from os import environ
from flask import Flask, make_response
from infra_utils.QueryInfradb import (available_slots,
                                      get_auto_reboot,
                                      get_ip,
                                      get_stbs_by_project,
                                      fetch_slots_versions,
                                      fetch_rack_slot_type_by_project,
                                      fetch_rack_slot_by_project_and_type,
                                      fetch_rack_slot_type_by_project_grouped_by_rack,
                                      fetch_rack_slot_by_project_and_type_grouped_by_rack)
from dotenv import load_dotenv

load_dotenv('.env', verbose=True)


app = Flask(__name__)

def hello():
    return environ.get("ENV")

@app.route("/")
def hello_world():
    return make_response(hello())

# missing endpoints  
# fetch_slots_versions_with_dinamic_filter
# get_auto_reboot (read before creating the endpoint)
# and from get_rack_slot_by_ip upwards

# tested with http://127.0.0.1:5000/available_slots/CERRI/Llama
@app.route("/available_slots/<proj>/<typ>")
def api_available_slots(proj, typ):
    return make_response(str(available_slots(proj,typ)))

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


# tested with http://127.0.0.1:5000/fetch_rack_slot_by_project_grouped_by_rack/PCC but also CERRI
@app.route("/fetch_rack_slot_type_by_project_grouped_by_rack/<proj>")
def api_fetch_rack_slot_type_by_project_grouped_by_rack(proj):
    # INITIALIZE CONNECTION TO DB and FETCH RSL info
    return fetch_rack_slot_type_by_project_grouped_by_rack(proj)

# tested with http://127.0.0.1:5000/fetch_rack_slot_by_project_and_type_grouped_by_rack/CERRI/Llama
@app.route("/fetch_rack_slot_by_project_and_type_grouped_by_rack/<proj>/<typ>")
def api_fetch_rack_slot_by_project_and_type_grouped_by_rack(proj, typ):
    return fetch_rack_slot_by_project_and_type_grouped_by_rack(proj,typ)

