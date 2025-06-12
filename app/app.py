from os import environ
from flask import Flask, make_response
from infra_utils.QueryInfradb import (fetch_rack_slot_type_by_project,
                                      fetch_rack_slot_type_by_project_grouped_by_rack,
                                      fetch_rack_slot_by_project_and_type_grouped_by_rack)
from settings import ENV

app = Flask(__name__)
app.config.from_pyfile('settings.py')

def hello():
    return ENV

@app.route("/")
def hello_world():
    return make_response(hello())