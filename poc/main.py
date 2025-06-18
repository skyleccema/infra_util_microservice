from flask import Flask, request
from flask_restx import Resource, Api, fields, marshal, reqparse

app = Flask(__name__)
api = Api(app)

todos = {}

@api.route('/<string:todo_id>')
class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}


### INTEGER HANDLER
int_model = api.model('IntegerModel', {
    'Integer': fields.Integer
})

class IntegerDao(object):
    def __init__(self, integer):
        self.integer = integer

def marshal_int(func_output: int, http_code: int) -> tuple[object, int]:
    try:
        if func_output is None:
            raise ValueError(func_output)
    except ValueError as e:
        app.logger.error(e)
        func_output = None
        http_code = 400
    return marshal(IntegerDao(func_output), int_model), http_code

@api.route('/availble_slots/<string:proj>/<string:typ>')
class GetAvaibleNum(Resource):
    def get(self, proj, typ):
        my_num = 2
        return marshal_int(func_output=my_num,http_code=200)


# Define the model
example_model = api.model('Example', {
    'id': fields.Integer(required=True, description='The unique identifier'),
    'data': fields.Raw(required=True, description='The dictionary data')
})

# # Define the request parser
# parser = reqparse.RequestParser()
# parser.add_argument('id', type=int, required=True, location='args')


@api.route('/example/<int:example_id>')
class ExampleResource(Resource):
    # @api.expect(parser)
    @api.marshal_with(example_model)
    def get(self, example_id):
        # args = parser.parse_args()

        # Retrieve the example data based on the provided ID
        example_data = {
            'id': example_id,
            'data': {'key1': 'value1', 'key2': 'value2'}
        }

        # Marshal the example data using the example_model
        return marshal(example_data, example_model)

if __name__ == '__main__':
    app.run(debug=True)