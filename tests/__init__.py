import unittest
from gradient import create_app, db
    

class Base(unittest.TestCase):
  '''
  Base test class for all tests to inherit from
  '''

  # executed prior to each test
  def setUp(self):

    # create app with 'environment=testing' param
    #   to use testing configurations
    self.app = create_app(environment="testing")  
    self.client = self.app.test_client()

    # assert that env is 'testing'
    self.assertEqual(self.app.env, "testing")

    # push context
    self._ctx = self.app.test_request_context()
    self._ctx.push()

    # reset db
    self.db = db
    with self.app.app_context():
      self.db.drop_all()
      self.db.create_all()


  # executed after each test
  def tearDown(self):
    pass


