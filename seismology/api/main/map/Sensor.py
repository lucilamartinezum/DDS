from main import ma
from marshmallow import fields, validate

class SensorSchema(ma.Schema):
    class Meta:
        fields = ("id_num", "name", "ip", "port", "status", "active", "user_id", "user")
    # _links = ma.Hyperlinks({"self": ma.URLFor("user_id", id="<userId>"), "collection": ma.URLFor("users")})
    user = fields.Nested(UserSchema(exclude={"password"}), dump_only=True)

