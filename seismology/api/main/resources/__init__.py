from .Sensor import Sensor as SensorResource
from .Sensor import Sensors as SensorsResource

from .Seism import Unverifiedseism as UnverifiedseismResource
from .Seism import Unverifiedseisms as UnverifiedseismsResource

from .Seism import Verifiedseism as VerifiedseismResource
from .Seism import Verifiedseisms as VerifiedseismsResource

from .User import User as UserResource
from .User import Users as UsersResource

"""from marshmallow import validate
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from main.models import UserModel

class User(SQLAlchemySchema):
    class Meta:
        model = UserModel
        include_relationships = True
        load_instance = True

    id = auto_field(dump_only=True)
    email = auto_field(required=True, validate.Email())
    admin = auto_field(required=True)
    password = auto_field(load_only=True)"""