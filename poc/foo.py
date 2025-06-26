from flask_restx import (Model, fields, Namespace,
                         ValidationError)
from typing import Any
from dataclasses import dataclass


@dataclass
class PersonalAddress(Model):
    address1 = fields.String(description="Personal Address1")
    address2 = fields.String(description="Personal Address2")

    @staticmethod
    def swagger_model(ns: Namespace) -> Any:
        if isinstance(ns, Namespace):
            return ns.model(
                name="Personal Address",
                model={
                    "address1": fields.String(description="Personal Address"),
                    "address2": fields.String(description="Personal Address2")
                }
            )
        else:
            raise ValidationError("Namespace object not defined.")


@dataclass
class Person(Model):
    person_id = fields.Integer(required=True, description="Person ID")
    name = fields.String(required=True, description="Person Name")
    age = fields.Integer(description="Person Age")
    address = fields.Nested(PersonalAddress,required=True, description="Person Address field")
    # address = fields.Raw(required=True, description="Person Address field")
    @staticmethod
    def swagger_model(ns: Namespace) -> Any:
        if isinstance(ns, Namespace):
            # check_tv_apps_fr_model = convert_schema_to_model(
            #     ns, TvAppsSchema, "Tv_Apps_History_Payload"
            # )
            return ns.model(
                name="Personal Address",
                model={
                    "person_id": fields.Integer(description="Person ID"),
                    "name": fields.String(description="Person Name"),
                    "age": fields.Integer(description="Person Age"),
                    "address": fields.Nested(PersonalAddress,description="Person Name")
                }
            )
        else:
            raise ValidationError("Namespace object not defined.")