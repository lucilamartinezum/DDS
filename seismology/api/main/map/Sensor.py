from main import ma
from marshmallow import fields, validate
from ..map.User import UserSchema


class SensorSchema(ma.Schema):
    class Meta:
        fields = ("id_num", "name", "ip", "port", "status", "active", "user_id", "user")
    user = fields.Nested(UserSchema(exclude={"password"}), dump_only=True)

