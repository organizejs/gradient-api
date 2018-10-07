from tests import Base
from gradient.models.user import UserModel
from gradient.models.customer import CustomerModel, MaritalStatus
import random


class Factory():


  def __init__(self, app, db):
    self.app = app
    self.db = db


  def create_user(self, 
      email=None,
      given_name=None,
      family_name=None
    ) -> "UserModel":
    '''
    this will create a user but bypass (google) oauth
    '''
    # generate unique identity each time
    alphabets = "abcdefghijklmnopqrstuvwxyz"
    suffix = ''.join(random.sample(alphabets, 10))

    email = "test_{}@mail.com".format(suffix) \
      if email is None else email 
    given_name = "test_{}@mail.com".format(suffix) \
      if given_name is None else given_name
    family_name = "test_{}@mail.com".format(suffix) \
      if family_name is None else family_name

    # create user
    user = UserModel(
      email,
      given_name,
      family_name
    )
    user.save()

    return user


  def create_customer(self,
      user=None,
      income=100,
      dependents=1,
      marital_status=MaritalStatus.SINGLE
    ) -> "CustomerModel":
    '''
    create a customer
    '''

    # create user if user is not provided
    if user is None:
      user = self.create_user()

    # create customer
    customer = CustomerModel(
      user=user,
      income=income,
      dependents=dependents,
      marital_status=marital_status
    )
    customer.save()

    return customer
    
    

    
