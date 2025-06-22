from flask import Flask
from flask_restx import Api, Resource, fields, marshal
app = Flask(__name__)
api = Api(app)
# Step 3: Define Models
# Model for the inner dictionary
field_model = api.model('Field', {
    'name': fields.String(required=True, description='The name field')
})
# Model for the outer dictionary
group_model = api.model('Group', {
    'field1': fields.String(required=True, description='The first field'),
    'fields2': fields.List(fields.Nested(field_model), description='List of fields2')
})
# Model for the main structure
main_model = api.model('Main', {
    'group': fields.List(fields.Nested(group_model), description='List of groups')
})
# Sample data
data = {
    "group": [
        {
            "field1": "val1",
            "fields2": [
                {"name": "value11"},
                {"name": "value12"}
            ]
        }
    ]
}
# Step 4: Create a Resource
@api.route('/data')
class DataResource(Resource):
    def get(self):
        # Step 5: Marshal the data
        return marshal(data, main_model), 200
if __name__ == '__main__':
    app.run(debug=True)