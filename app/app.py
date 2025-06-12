from os import environ
from flask import Flask, make_response
from infra_utils.QueryInfradb import (fetch_rack_slot_type_by_project,
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

@app.route("/fetch_rack_slot_type_by_project_c")
def get_rack_slot_type_by_project_c():
    # return make_response("ARRRRG")
    # INITIALIZE CONNECTION TO DB
    # FETCH THE TYPE

    return fetch_rack_slot_type_by_project("CERRI")
    # return fetch_rack_slot_type_by_project("PCC")

@app.route("/fetch_rack_slot_type_by_project_p")
def get_rack_slot_type_by_project_p():
    # return make_response("ARRRRG")
    # INITIALIZE CONNECTION TO DB
    # FETCH THE TYPE

    return fetch_rack_slot_type_by_project("PCC")
    # return fetch_rack_slot_type_by_project("PCC")
