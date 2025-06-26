from marshmallow import fields as ma_fields, ValidationError, Schema, validates_schema
from flask_restx import fields as fr_fields
from marshmallow.validate import OneOf

from dataclasses import dataclass


def convert_schema_to_model(api, schema, name):
    """
    Utility to convert a Marshmallow schema into a Flask-RESTx model

    :param api: Instance of Flask-RESTx API
    :param schema: Marshmallow schema to convert
    :param name: Name of the Flask-RESTx model
    :return: Flask-RESTx model
    """

    # Map Marshmallow field types to corresponding Flask-RESTx field types
    mapping = {
        ma_fields.String: fr_fields.String,
        ma_fields.Int: fr_fields.Integer,
        ma_fields.DateTime: fr_fields.DateTime,
        ma_fields.List: fr_fields.List,
    }

    model_fields = {}
    for field_name, field in schema().fields.items():
        if hasattr(field, "validate") and isinstance(field.validate, OneOf):
            description = "One of: {}".format(
                ", ".join(map(str, field.validate.choices))
            )
        if isinstance(field, ma_fields.List):
            # inner_field = mapping.get(type(field.inner))
            # if type(field.inner) in mapping else fr_fields.Raw
            if type(field.inner) in mapping:
                inner_field = mapping.get(type(field.inner))()
            elif type(field.inner) is ma_fields.Nested:
                nested_model = convert_schema_to_model(
                    api, field.inner.nested, field_name
                )
                inner_field = fr_fields.Nested(nested_model, required=field.required)
            else:
                inner_field = fr_fields.Raw()
            model_fields[field_name] = fr_fields.List(
                inner_field, required=field.required
            )
        elif isinstance(field, ma_fields.Nested):
            nested_model = convert_schema_to_model(api, field.nested, field_name)
            model_fields[field_name] = fr_fields.Nested(
                nested_model, required=field.required
            )
        else:
            model_fields[field_name] = mapping[type(field)](required=field.required)

    # model_fields["test_steps"] = fr_fields.List(fr_fields.Nested(
    #     fr_fields.String ), required=field.required)
    print(model_fields)
    return api.model(name, model_fields)

############################################################################

@dataclass
class Address:
    address1: ma_fields.String
    address2: ma_fields.String

class AddressSchema(Schema):
    address1: ma_fields.String = ma_fields.String(required=True)
    address2: ma_fields.String = ma_fields.String(required=True)
# class _NestedObject(ma_fields.Field, fr_fields.Raw):
#     address1: ma_fields.String = ma_fields.String(required=True)
#     address2: ma_fields.String = ma_fields.String(required=True)

# @dataclass
# class PersonDC:
#     person_id: ma_fields.Integer
#     name: ma_fields.String
#     age: ma_fields.Integer
#     address: ma_fields.List
#
# class PersonSchema(Schema):
#     person_id: ma_fields.Integer = ma_fields.Integer(required=True)
#     name: ma_fields.String = ma_fields.String(required=True)
#     age: ma_fields.Integer = ma_fields.Integer(required=True)
#     address: ma_fields.List = ma_fields.List(_NestedObject(),required=True)


# class TvAppsSchema(Schema):
#     __server_names: list = [
#         "STHD 01",
#         "STHD 02",
#         "STHD 03",
#         "STHD 04",
#         "STHD 05",
#         "STHD 06",
#         "STHD 07",
#         "MQ781",
#         "MQ782",
#         "MQ783",
#         "4.0 META3",
#         "MQ723",
#         "MQ784",
#         "MQ785",
#         "MQ786",
#         "4.0 META2",
#         "4.0 META4",
#         "4.0 META7",
#         "4.0 META5C",
#         "MQ819 DE"
#     ]
#
#     __device_types: list = ["GLASS", "SKYQ", "MYSKY"]
#     __infra_device_types: list = [
#         "Xi1",
#         "Llama",
#         "Stream",
#         "Falcon",
#         "Amidala",
#         "Amidala_Hip",
#         "Titan",
#         "MRBOX",
#         "MySkyHD",
#         "OpenTV",
#         "Roku",
#         "Sky+",
#         "X-Wing"
#     ]
#
#     __slots: list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
#
#     test_name: ma_fields.String = ma_fields.String(required=True)
#     project_name: ma_fields.String = ma_fields.String(required=True)
#     device_type: ma_fields.String = ma_fields.String(required=True, validate=OneOf(__device_types))
#     infra_device_type: ma_fields.String = ma_fields.String(required=False, validate=OneOf(__infra_device_types))
#     start_time: ma_fields.DateTime = ma_fields.DateTime(required=True)
#     max_duration: ma_fields.Integer = ma_fields.Integer(required=True)
#     server_name: ma_fields.String = ma_fields.String(required=True, validate=OneOf(__server_names))
#     slot: ma_fields.Integer = ma_fields.Integer(required=True, validate=OneOf(__slots))
#     test_steps: ma_fields.List = ma_fields.List(_NestedObject(), required=True)
#
#     @validates_schema
#     def validate_settings(self, data, **kwargs):
#         global __device_types
#         __common_actions = ["capture_screen", "sleep", "power_cycle", "ocr", "ocr_until", "capture_log", "dynamic_path"]
#         __device_type_mapping = {
#             "Xi1": "Verdi",
#             "Llama": "GLASS",
#             "Stream": "Sky Stream",
#             "Falcon": "SKYQ",
#             "Amidala": "SKYQ",
#             "Amidala_Hip": "SKYQ",
#             "Titan": "SKYQ",
#             "MRBOX": "SKYQ",
#             "MySkyHD": "MYSKY",
#             "OpenTV": "Open Tv",
#             "Roku": "Now Tv",
#             "Sky+": "Sky plus ENG",
#             "X-Wing": "SKYQ ENG"
#         }
#         __valid_infra_device_type = ["Llama", "Falcon", "Amidala", "Amidala_Hip", "Titan", "MRBOX", "MySkyHD"]
#         __infra_device_type = data.get('infra_device_type', None)
#
#         if __infra_device_type is not None:
#             print(f"__infra_device_type {__infra_device_type}")
#             __device_type = __device_type_mapping.get(__infra_device_type, None)
#             print(f"__device_type {__device_type}")
#             if __infra_device_type not in __valid_infra_device_type:
#                 raise ValidationError(
#                     f"Please use one of the following infra_device_type {__valid_infra_device_type} ")
#         else:
#             __device_type = data.get('device_type')
#
#         if __device_type is None:
#             raise ValidationError(
#                 f"Please use one of the following infra_device_type {__device_types} ")
#
#         if __device_type == "SKYQ":
#             for step in data.get("test_steps"):
#                 __skyq_valid_actions = __common_actions.copy()
#                 __skyq_valid_actions.append('press_buttons_skyq')
#                 __ac = step.action
#                 if __ac not in __skyq_valid_actions:
#                     raise ValidationError(f"Action {__ac} not valid for SKYQ, "
#                                           f"please use one of the following {__skyq_valid_actions}")
#         if __device_type == "GLASS":
#             for step in data.get("test_steps"):
#                 __glass_valid_actions = __common_actions.copy()
#                 __glass_valid_actions.append('press_buttons_glass')
#                 __ac = step.action
#                 if __ac not in __glass_valid_actions:
#                     raise ValidationError(f"Action {__ac} not valid for GLASS, "
#                                           f"please use one of the following {__glass_valid_actions}")
#         if __device_type == "MYSKY":
#             for step in data.get("test_steps"):
#                 __mysky_valid_actions = __common_actions.copy()
#                 __mysky_valid_actions.append('press_buttons_mysky')
#                 __ac = step.action
#                 __mysky_valid_actions.remove("capture_log")
#                 __mysky_valid_actions.remove("dynamic_path")
#                 if __ac not in __mysky_valid_actions:
#                     raise ValidationError(f"Action {__ac} not valid for MYSKY, "
#                                           f"please use one of the following {__mysky_valid_actions}")




# class _NestedObject(ma_fields.Field, fr_fields.Raw):
#     @staticmethod
#     def _message(value: str) -> str:
#         return f"""{value}:
#     please use one of the following action :
#         press_buttons_skyq,
#         press_buttons_mysky,
#         press_buttons_glass,
#         capture_screen,
#         sleep,
#         power_cycle,
#         ocr_until,
#         ocr,
#         capture_log,
#         dynamic_path
#     """
#
#     def _deserialize(self, value, attr, data, **kwargs):
#         action = value.get("action")
#         if action is not None:
#             # print("INNER ACTION", action)
#             chain = HandleActionsChain()
#             chain.add_handler(HandleButtonsSkyQ())
#             chain.add_handler(HandleButtonsMySky())
#             chain.add_handler(HandleButtonsGlass())
#             chain.add_handler(HandleCaptureScreen())
#             chain.add_handler(HandleSleep())
#             chain.add_handler(HandlePowerCycle())
#             chain.add_handler(HandleOCRUntil())
#             chain.add_handler(HandleOCR())
#             chain.add_handler(HandleCaptureLog())
#             chain.add_handler(HandleDynamicPath())
#             chain.add_handler(HandleValidationError())
#             return chain.handle_actions(action, value)
#         else:
#             raise ValidationError(get_nested_actions()._message(value=value))
#
#
# def get_nested_actions() -> _NestedObject:
#     return _NestedObject()