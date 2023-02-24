from constants import MOVIES_PER_PAGE
from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_all(self, filters):
        page = filters.get('page')
        query = self.session.query(User)

        if not page:
            return query.all()

        return query.paginate(page=page, per_page=MOVIES_PER_PAGE, error_out=False).items

    def get_by_email(self, val):
        return self.session.query(User).filter(User.email == val).first()

    def create(self, user_d):
        ent = User(**user_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

    def patch_update(self, user_d):
        user = self.get_one(user_d.get("id"))
        if 'name' in user_d:
            user.name = user_d.get("name")
        if 'surname' in user_d:
            user.surname = user_d.get("surname")
        if 'email' in user_d:
            user.email = user_d.get("email")
        if 'favorite_genre_id' in user_d:
            user.favorite_genre_id = user_d.get("favorite_genre_id")

        self.session.add(user)
        self.session.commit()

    def password_update(self, user_d):
        user = self.get_one(user_d.get("id"))
        user.password = user_d.get("new_password")
        self.session.add(user)
        self.session.commit()