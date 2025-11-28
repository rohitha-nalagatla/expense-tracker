from marshmallow import Schema, fields

class ExpenseSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Str(required=True)
    category_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    description = fields.Str()
    date = fields.Date(required=True)

class UpdateExpenseSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Str(required=True)
    category_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    description = fields.Str()
    date = fields.Date(required=True)