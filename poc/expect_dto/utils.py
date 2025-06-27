import sys

from flask_restx import Api, Model
from typing import Any
import traceback
# generic model
def im(api: Api, name: str, schema_model: Any) -> Model:
    return  api.model(
        name, schema_model
    )

def validate_pietro(msg: str):
    try:
        #msg = msg.upper()

        if msg == "PIETRO":
            msg = msg.lower()
        else:
            raise ValueError(msg)
    except ValueError as e:
        raise ValueError("No Pietro inputtt!!")

