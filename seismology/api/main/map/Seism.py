from main import ma
from marshmallow import fields, validate


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
