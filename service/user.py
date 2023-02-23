import base64
import hashlib
import hmac

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
        if filters.get("email") is not None:
            users = self.dao.get_by_email(filters.get("email"))
        else:
            users = self.dao.get_all()
        return users

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

    def update(self, user_d):
        user_d['password'] = self.get_hash(user_d['password'])
        self.dao.update(user_d)
        return self.dao
