from tests import Base
from gradient.models.user import UserModel


class Factory():


  def __init__(self, app, db):
    self.app = app
    self.db = db


  def create_user(self, email, given_name, family_name):
    '''
    this will create a user but bypass (google) oauth
    '''
    self.app
    user = UserModel(
      email,
      given_name,
      family_name
    )
    user.save()

