from tests import Base
from .factory import Factory
from gradient.models.user import UserModel


class TestUser(Base):

  def test_empty_users(self):
    '''
    test /users endpoint when no users
    '''
    res = self.client.get('/users')
    self.assertEqual(res.status_code, 404)


  def test_non_empty_users(self):
    '''
    test /users endpoint when there exists users
    '''
    factory = Factory(self.app, self.db)
    factory.create_user()
    res = self.client.get('/users')
    self.assertEqual(res.status_code, 200)
