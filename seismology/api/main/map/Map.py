from main import ma

class SensorSchema(ma.Schema):
    class Meta:
        fields = ("id_num", "name", "ip", "port", "status", "active", "user_id","_links", "user")
    _links = ma.Hyperlinks({"self": ma.URLFor("user_id", id="<userId>"), "collection": ma.URLFor("users")})
