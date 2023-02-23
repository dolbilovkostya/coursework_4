from flask import request
from flask_restx import Resource, Namespace
from implemented import auth_service, user_service

auth_ns = Namespace('auth')


@auth_ns.route('/register')
class AuthRegView(Resource):
    def post(self):
        req_json = request.json

        email = req_json.get('email', None)
        password = req_json.get('password', None)

        if None in [email, password]:
            return '', 404

        user_service.create(req_json)
        return 201


@auth_ns.route('/login')
class AuthLogView(Resource):
    def post(self):
        req_json = request.json

        email = req_json.get('email', None)
        password = req_json.get('password', None)

        if None in [email, password]:
            return '', 404

        tokens = auth_service.generate_tokens(email, password)

        return tokens, 201
    #
    # def put(self):
    #     req_json = request.json
    #     token = req_json.get('refresh_token')
    #
    #     if token is None:
    #         return '', 404
    #
    #     tokens = auth_service.approve_refresh_token(token)
    #
    #     return tokens, 201
