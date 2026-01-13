from marshmallow import Schema, fields


class BudgetSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Str(required=True)
    category_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    month = fields.Int(required=True)
    year = fields.Int(required=True)

class UpdateBudgetSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Str(required=True)
    category_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    month = fields.Int(required=True)
    year = fields.Int(required=True)