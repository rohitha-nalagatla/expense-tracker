from marshmallow import Schema, fields, validate

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    category_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category_type = fields.Str(required=True, validate=validate.OneOf(['income', 'expense']))
    description = fields.Str(validate=validate.Length(max=255))
    created_at = fields.DateTime(dump_only=True)

class CategoryResponseSchema(Schema):
    id = fields.Int()
    category_name = fields.Str()
    category_type = fields.Str()
