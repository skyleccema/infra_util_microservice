from flask import Flask
from flask_restx import Api, Resource, fields, Namespace
from marshmallow import Schema, fields as ma_fields

from utils import *

app = Flask(__name__)
api = Api(app)

my_ns = Namespace('MSG CHECKER',path='.',description='Msg check API')


class MsgSchema(Schema):
    person = ma_fields.String(required=True, validate=lambda x: x!="PIETRO")


@api.route('/hello')
class MyHello(Resource):
    @api.expect(im(api, 'hello input model', {'person': fields.String(required=True,validate=lambda x:validate_pietro(x))}))
    # @api.expect(im(api, 'hello input model', {'person': fields.String(required=True,validate=lambda x: x!="Pietro")}))
    def post(self):
        data = api.payload['person']
        return 'hello ' + data + '!'