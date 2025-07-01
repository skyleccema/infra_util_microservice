#/query_stb_info
from marshmallow import fields as ma_fields, Schema, validate
from .utils import project_validator, hw_type_validator

class FetchRackSlotTypeByProjectSchemaIn(Schema):
    project = ma_fields.Str(
        required=True,
        validate=lambda x:project_validator(x)
    )

