from flask_restful import Resource, abort
from ..models import UserModel, UserSchema


class User(Resource):

  def get(self, user_id):
    user = UserModel.get(user_id)
    if user is None:
      abort(404, message="No user with id {} exists.".format(user_id))
    user_data = UserSchema().dump(user).data
    return user_data


class UserList(Resource):

  def get(self):
    users = UserModel.get_all()
    if users is None or len(users) <= 0:
      abort(404, message="No users exist.")
    users_data = UserSchema(many=True).dump(users).data
    return users


