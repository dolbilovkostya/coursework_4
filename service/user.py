import base64
import hashlib
import hmac

from flask_restx import abort

from dao.user import UserDAO
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_by_email(self, email):
        return self.dao.get_by_email(email)

    def get_all(self, filters):
        return self.dao.get_all(filters)


    def delete(self, rid):
        self.dao.delete(rid)


    def get_hash(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return base64.b64encode(hash_digest)


    def compare_passwords(self, hash, password):
        decoded_digest = base64.b64decode(hash)

        hash_digest = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                PWD_HASH_SALT,
                PWD_HASH_ITERATIONS
                )

        return hmac.compare_digest(decoded_digest, hash_digest)

    def create(self, user_d):
        user_d['password'] = self.get_hash(user_d['password'])
        return self.dao.create(user_d)

    def patch_update(self, user_d):
        # if 'password' in user_d:
        #     user_d['password'] = self.get_hash(user_d['password'])
        self.dao.patch_update(user_d)
        return self.dao

    def password_update(self, user_d):
        if not self.compare_passwords(password=user_d['current_password'], hash=self.get_one(user_d['id']).password):
            abort(401, "Provided current password is not correct")

        user_d['new_password'] = self.get_hash(user_d['new_password'])
        self.dao.password_update(user_d)
        return self.dao
