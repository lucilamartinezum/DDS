from main import ma
from marshmallow import fields, validate


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    email = fields.String(required=True, validate=validate.Email())
    admin = fields.Boolean(required=True, falsy={0, 'false', 'False', 'FALSE'}, truthy={'true', 1, 'TRUE', 'True'})
    password = fields.String(required=True)


class SensorSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "ip", "port", "status", "active", "user_id", "user")

    user = fields.Nested(UserSchema(exclude={"password"}), dump_only=True)


class SeismSchema(ma.Schema):
    datetime = fields.DateTime("%Y-%m-%dT%H:%M:%S", required=True)
    depth = fields.String(required=True)
    magnitude = fields.Float(required=True)
    id = fields.Int(dump_only=True)
    latitude = fields.Str(required=True)
    longitude = fields.Str(required=True)
    verified = fields.Bool(required=True)
    sensorId = fields.Int(required=True)
    sensor = fields.Nested(SensorSchema(), dump_only=True)
