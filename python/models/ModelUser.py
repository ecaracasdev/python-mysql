from utils.db import User
from .entities.User import EUser


class ModelUser():

    @classmethod
    def login(self, user):
        try:
            admin_user = User.query.filter_by(username=user.username).first()
            if admin_user:
                user = EUser(admin_user.id, admin_user.username, EUser.check_password(
                    self, hashed_password=admin_user.password, password=user.password), admin_user.fullname)
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, id):
        try:
            admin_user = User.query.filter_by(id=id).first()
            if admin_user:
                user = EUser(admin_user.id, admin_user.username,
                             None, admin_user.fullname)
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
