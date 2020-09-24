from main.map.Map import SeismSchema
from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SeismModel
from main.models import SensorModel
import time
from random import uniform, random, randint
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required
from main.resources.Pagination import Pagination

seism_schema = SeismSchema()
seism_schema = SeismSchema(many=True)


class UnverifiedSeism(Resource):

    # @jwt_required
    # obtener recurso
    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            return seism_schema.jsonify(seism)
        else:
            return 'Denied Access', 403

    @admin_required
    # eliminar recurso
    def delete(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            db.session.delete(seism)
            db.session.commit()
            return 'Unverifield seism was delete succesfully', 204
        else:
            return 'Denied Access', 403

    @admin_required
    # modificar recurso
    def put(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            for key, value in request.get_json().items():
                setattr(seism, key, value)
            db.session.add(seism)
            db.session.commit()
            return seism.to_json(), 201
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
        return seism_schema.dump(query.all())

    @admin_required
    def post(self):
        sensors = db.session.query(SensorModel).all()
        sensorsId = []
        for sensor in sensors:
            sensorsId.append(sensor.id)

        value_sensor = {
            'datetime': time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()),
            'depth': randint(5, 250),
            'magnitude': round(uniform(2.0, 5.5), 1),
            'latitude': uniform(-180, 180),
            'longitude': uniform(-90, 90),
            'verified': False,
            'sensorId': sensorsId[randint(0, len(sensorsId) - 1)]
        }
        seism = SeismModel.from_json(value_sensor)
        db.session.add(seism)
        db.session.commit()
        return seism.to_json(), 201


class VerifiedSeism(Resource):
    @jwt_required
    # obtener recurso
    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if seism.verified:
            return seism_schema.jsonify(seism)
        else:
            return 'Denied Access', 403


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
        return seism_schema.dump(query.all())
