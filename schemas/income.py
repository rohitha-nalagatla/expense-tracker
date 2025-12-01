from marshmallow import Schema, fields

class IncomeSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Str(dump_only=True)  # Don't require from request, set from JWT
    amount = fields.Float(required=True)
    category_id = fields.Int(required=True)
    description = fields.Str()
    date = fields.Date(required=True)

class UpdateIncomeSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Str(dump_only=True)  # Don't require from request, set from JWT
    category_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    description = fields.Str()
    date = fields.Date(required=True)