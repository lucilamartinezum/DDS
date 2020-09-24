from main import ma
from marshmallow import fields, validate


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    email = fields.String(required=True, validate=validate.Email())
    admin = fields.Boolean(required=True, falsy={0, 'false', 'False', 'FALSE'}, truthy={'true', 1, 'TRUE', 'True'})
    password = fields.String(required=True)
