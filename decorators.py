import jwt
from flask import abort, request

from constants import JWT_SECRET, JWT_ALGO


def auth_required(function):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]

        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])

        except Exception as e:
            print('JWT decode exception', e)
            abort(401)

        return function(*args, **kwargs)

    return wrapper