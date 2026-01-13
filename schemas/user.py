from marshmallow import Schema, fields, validate

class UserRegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=30))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    full_name = fields.Str()
    age = fields.Int()

class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class UserResponseSchema(Schema):
    username = fields.Str()
    email = fields.Email()
    full_name = fields.Str()
    age = fields.Int()
