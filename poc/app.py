import dataclasses
from dataclasses import dataclass

from flask import Flask
from flask_restx import (Api, Resource, fields, Model,
                         Namespace, ValidationError , marshal)
from typing import Any
from action_utils import convert_schema_to_model, AddressSchema


app = Flask(__name__)
api = Api(app)



@api.route('/persons')
class PersonList(Resource):
    def get(self):
        class CustomField(fields.Raw):
            def __init__(self, myobj):
                self.myobj = myobj
            def output(self, key, obj, **kwargs):
                return self.myobj.__repr__()

        person_model = {
            'pid': fields.Integer,
            'name': fields.String,
            'age': fields.Integer,
            'address': CustomField,
        }

        class Person:
            def __init__(self, pid: int, name: str, age: int):
                self.pid = pid
                self.name = name
                self.age = age
                self.address = None

        persons = [
            Person(1, 'John', 30),
            Person(2, 'Jane', 25),
            Person(3, 'Bob', 35)
        ]
        return marshal(persons, person_model, envelope="people")


if __name__ == '__main__':
    app.run(debug=True)

#### Working but no object marshalled?
# address_model = api.model(
#     'address model', {
#         'addr1': fields.String,
#         'addr2': fields.String,
#     }
# )
#
# person_model = api.model(
#     'person model', {
#         'pid': fields.Integer,
#         'name': fields.String,
#         'age': fields.Integer,
#         'address': fields.Nested(address_model)
#     }
# )
#
# class Address:
#     def __init__(self, addr1: str, addr2: str):
#         self.addr1 = addr1
#         self.addr2 = addr2
#
# class Person:
#     def __init__(self, pid: int, name: str, age: int, address: Address):
#         self.pid = pid
#         self.name = name
#         self.age = age
#         self.address = address
#
# @api.route('/persons')
# class PersonList(Resource):
#     def get(self):
#         persons = [
#             Person(1, 'John', 30, Address("via via", "via via2")),
#             Person(2, 'Jane', 25, Address("via qui", "via qui2")),
#             Person(3, 'Bob', 35, Address("via qua", "via qua2"))
#         ]
#         return marshal(persons, person_model, envelope="people")
