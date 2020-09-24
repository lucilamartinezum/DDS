from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SensorModel
from main.models import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required
from main.map.Sensor import SensorSchema
from main.resources.Pagination import Pagination

sensor_schema = SensorSchema()
sensor_schema = SensorSchema(many = True)

class Sensor(Resource):
    @jwt_required
    #obtener recurso
    def get(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        return sensor_schema.jsonify(sensor)
    @admin_required
    #eliminar recurso
    def delete(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        db.session.delete(sensor)
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return '', 409
        return "Sensor was deleted succesfully", 204
    @admin_required
    #modificar recurso
    def put(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        data = sensor_schema.load(request.get_json())
        for key, value in data:
            setattr(sensor, key, value)
        db.session.add(sensor)
        try:
            db.session.commit()
            return sensor_schema.jsonify(sensor), 201
        except Exception as error:
            return str(error), 400


class Sensors(Resource):
    #@jwt_required
    #obtener lista de recursos
    def get(self):
        query = db.session.query(SensorModel)
        page_number = 1
        elem_per_page = 25
        #max_per_page = 50
        pag = Pagination(query, page_number, elem_per_page)
        for key, value in request.get_json().items:
            query = pag.apply(key, value)
        query, pagination = pag.pagination()
        return sensor_schema.dump(query.all())
    @admin_required
    #insertar recurso
    def post(self):
        data = sensor_schema.load(request.get_json())
        sensor = SensorModel(name=data['name'], ip =data["ip"], port=data["port"], status=data["status"], active=data["active"], userId=data["userId"])
        try:
            db.session.add(sensor)
            db.session.commit()
        except Exception as error:
            return str(error), 400
        return sensor.to_json(), 201

