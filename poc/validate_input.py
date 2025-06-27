from flask import Flask
from flask_restx import Api, Resource, fields
from marshmallow import Schema, fields as ma_fields, validate, ValidationError
import sys


class UserRegistrationSchema(Schema):
    username = ma_fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=50,
                            error='Username must be between 3 and 50 characters'),
            validate.Regexp(r'^[a-zA-Z0-9_]+$',
                            error='Username can only contain letters, numbers, and underscores')
        ]
    )
    email = ma_fields.Email(
        required=True,
        validate=validate.Email(error='Invalid email format')
    )
    password = ma_fields.Str(
        required=True,
        validate=[
            validate.Length(min=8, error='Password must be at least 8 characters'),
            validate.Regexp(
                r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
                error='Password must include letters, numbers, and special characters'
            )
        ]
    )


class UserRegistrationResource(Resource):
    def __init__(self, *args, **kwargs):
        self.schema = UserRegistrationSchema()
        super().__init__(*args, **kwargs)

    def post(self):
        try:
            # Validate input
            data = self.schema.load(api.payload)
            # data = self.schema.load(request.json)

            # If validation passes, proceed with user registration
            # Your user creation logic here
            return {
                'message': 'User registered successfully',
                'user': data
            }, 201

        except ValidationError as err:
            # Return validation errors
            return {
                'message': 'Validation Error',
                'errors': err.messages
            }, 400


# Flask-RESTx setup
app = Flask(__name__)
api = Api(app)

# Add resource to API
api.add_resource(UserRegistrationResource, '/register')

if __name__ == '__main__':
    try:
        print('hi guyzzzz',file=sys.stderr)
        app.run(debug=True)
    except ValueError as e:
        print('Error, bye guyzzzz')
        app.logger.error(e,)