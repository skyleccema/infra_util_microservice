from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

# Define the class for the person object
class Person:
    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age

# Define the fields for a single object
person_fields = api.model('Person', {
    'id': fields.Integer,
    'name': fields.String,
    'age': fields.Integer,
    'ref': fields.Raw(attribute=lambda x: str(x))
})

# Define the fields for a list of objects
person_list_fields = api.model('PersonList', {
    'persons': fields.List(fields.Nested(person_fields))
})

@api.route('/persons')
class PersonList(Resource):
    @api.marshal_with(person_list_fields)
    def get(self):
        persons = [
            Person(1, 'John', 30),
            Person(2, 'Jane', 25),
            Person(3, 'Bob', 35)
        ]
        return {'persons': persons}

if __name__ == '__main__':
    app.run(debug=True)