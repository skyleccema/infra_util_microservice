from flask import Flask, make_response
from infra_utils.QueryInfradb import (fetch_rack_slot_type_by_project,
                                      fetch_rack_slot_type_by_project_grouped_by_rack,
                                      fetch_rack_slot_by_project_and_type_grouped_by_rack)
app = Flask(__name__)

def hello():
    return "Hello vov"

@app.route("/")
def hello_world():
    return make_response(hello())