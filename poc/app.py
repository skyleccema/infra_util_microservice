from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

# Define the model for the dictionary
dictionary_model = api.model('Dictionary', {
    'key': fields.String(required=True, description='The key of the dictionary'),
    'value': fields.String(required=True, description='The value of the dictionary')
})

# Define the resource and the endpoint
@api.route('/dictionaries')
class DictionaryList(Resource):
    def get(self):
        """
        Retrieve a list of dictionaries
        """
        dictionaries = get_dictionaries()
        # return api.marshal(dictionaries, fields.List(fields.Nested(dictionary_model)))
        return api.marshal(dictionaries, dictionary_model)#for i in dictionary_model: fields.Nested(i))

def get_dictionaries():
    """
    Function to retrieve a list of dictionaries
    """
    return [
        {'key': 'key1', 'value': 'value1'},
        {'key': 'key2', 'value': 'value2'},
        {'key': 'key3', 'value': 'value3'}
    ]

if __name__ == "__main__":
    app.run(debug=True)