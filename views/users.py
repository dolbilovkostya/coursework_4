from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        name = request.args.get("name")
        surname = request.args.get("surname")
        password = request.args.get("password")
        email = request.args.get("email")
        favorite_genre_id = request.args.get("favorite_genre_id")
        filters = {
            "name": name,
            "surname": surname,
            "password": password,
            "email": email,
            "favorite_genre_id": favorite_genre_id
        }
        all_users = user_service.get_all(filters)
        res = UserSchema(many=True).dump(all_users)
        return res, 200

    def post(self):
        req_json = request.json
        user = user_service.create(req_json)
        return "", 201, {"location": f"/users/{user.id}"}


@user_ns.route('/<int:bid>')
class UserView(Resource):
    def get(self, bid):
        b = user_service.get_one(bid)
        sm_d = UserSchema().dump(b)
        return sm_d, 200

    def put(self, bid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = bid
        user_service.update(req_json)
        return "", 204

    def delete(self, bid):
        user_service.delete(bid)
        return "", 204
