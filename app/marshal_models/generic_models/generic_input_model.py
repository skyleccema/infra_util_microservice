from flask import Flask
from flask_restx import Api, Model
from typing import Any

# generic model
def im(api: Api, name: str, schema_model: Any) -> Model:
    return  api.model(
        name, schema_model
    )