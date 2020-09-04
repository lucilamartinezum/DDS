from flask_restful import Resource
from flask import request, jsonify
from .. import db
from marshmallow import validate
from main.models import UserModel
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, jwt_optional
from main.map import UserSchema
from main.resources.Pagination import Pagination

user_schema = UserSchema()
user_schema = UserSchema(many = True)

class User(Resource):

    @jwt_required
    def get(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        return user.to_json()

    @jwt_required
    def put(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        for key, value in request.get_json().items():
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201

    @jwt_required
    def delete(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return '', 409
        return "User was deleted succesfully", 204

class Users(Resource):

    @jwt_required
    def get(self):
        query = db.session.query(UserModel)
        page_number = 1
        elem_per_page = 3
        pag = Pagination(query, page_number, elem_per_page)
        for key, value in request.get_json().items:
            query = pag.apply(key, value)
        query, pagination = pag.pagination()
        return user_schema.dump(query.all())

    #@admin_required
    def post(self):
        try:
            user = user_schema.load(request.get_json(), session=db.session)
            email_exists = db.session.query(UserModel).filter(UserModel.email == user.email).scalar() is not None
            if email_exists:
                return 'The entered email address has already been registered', 409
            else:
                db.session.add(user)
                db.session.commit()
                return user_schema.dump(user), 201
        except validate.ValidationError as e:
            return e, 409



