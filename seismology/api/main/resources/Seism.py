from main.map.Seism import SeismSchema
from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SeismModel
from main.models import SensorModel
import datetime
from random import uniform, randint
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required
from main.resources.Pagination import Pagination

seism_schema = SeismSchema()
seisms_schema = SeismSchema(many=True)


class UnverifiedSeism(Resource):

    # @jwt_required
    # obtener recurso
    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            return seism_schema.dump(seism)
        else:
            return 'Denied Access: not an unverified seism', 403

    # @admin_required
    # eliminar recurso
    def delete(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            db.session.delete(seism)
            db.session.commit()
            return 'Unverifield seism was delete succesfully', 204
        else:
            return 'Denied Access', 403

    # @admin_required
    # modificar recurso
    def put(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            for key, value in request.get_json().items():
                setattr(seism, key, value)
            db.session.add(seism)
            db.session.commit()
            return seism_schema.jsonify(seism), 201
        else:
            return 'Denied Access', 403


class UnverifiedSeisms(Resource):
    # @jwt_required
    # obtener lista de recursos
    def get(self):
        page_number = 1
        elem_per_page = 25
        filters = request.get_json().items()
        query = db.session.query(SeismModel).filter(SeismModel.verified == False)
        pag = Pagination(query, page_number, elem_per_page)
        for key, value in filters:
            query = pag.apply(key, value)
        query, pagination = pag.pagination()
        return seisms_schema.jsonify(query.all())

    # @admin_required
    def post(self):
        while True:
            sensors = db.session.query(SensorModel).all()
            sensorsId = []
            for sensor in sensors:
                sensorsId.append(sensor.id)
            value_sensor = {
                'datetime': datetime.datetime.now(),
                'depth': randint(20, 600),
                'magnitude': round(uniform(1, 9), 1),
                'latitude': uniform(-57.409798, 10.075782),
                'longitude': uniform(-87.475526, -55.477882),
                'verified': False,
                'sensorId': sensorsId[randint(0, len(sensorsId) - 1)]
            }
            seism_dumped = seisms_schema.dumps(value_sensor)
            seism = seisms_schema.loads(seism_dumped)
            db.session.add(seism)
            db.session.commit()
            return seism_schema.jsonify(seism), 201


class VerifiedSeism(Resource):
    # @jwt_required
    # obtener recurso
    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if seism.verified:
            return seism_schema.jsonify(seism)
        else:
            return 'Denied Access: not a verified seism', 403


class VerifiedSeisms(Resource):
    # @jwt_required
    # obtener lista de recursos
    def get(self):
        page_number = 1
        elem_per_page = 50
        filters = request.get_json().items()
        query = db.session.query(SeismModel).filter(SeismModel.verified == True)
        pag = Pagination(query, page_number, elem_per_page)
        for key, value in filters:
            query = pag.apply(key, value)
        query, pagination = pag.pagination()
        return seisms_schema.dump(query.all())
