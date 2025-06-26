from flask import Flask
from flask_restx import Api, Resource, fields, marshal
from dataclasses import dataclass, field

from typing import List

@dataclass
class MyInputData:
    name: str
    age: int
    hobbies: List[str] = field(default_factory=list)


app = Flask(__name__)
api = Api(app)

my_input_model = api.model('MyInputData', {
    'name': fields.String(required=True),
    'age': fields.Integer(required=True),
    'hobbies': fields.List(fields.String)
})


@api.route('/my-endpoint')
class MyEndpoint(Resource):
    @api.expect(my_input_model, validate=True)
    # @api.marshal_with(my_input_model)
    def post(self):
        data = MyInputData(**api.payload)
        # Validate the data
        if data.age < 0:
            return {'error': 'Age cannot be negative'}, 400
        if not data.hobbies:
            return {'error': 'At least one hobby is required'}, 400

        # Process the data
        # ...

        output_data = MyInputData(
            name=data.name,
            age=data.age,
            hobbies=data.hobbies
        )

        # return {'message': 'Data processed successfully'}, 200
        # return output_data, 200
        return marshal(output_data, my_input_model)
