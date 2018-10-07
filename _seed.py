'''
Development purposes only
'''

from gradient import create_app, db
from tests.factory import Factory


if __name__ == "__main__":

  app = create_app()

  with app.app_context():
    factory = Factory(app, db)

    customer0 = factory.create_customer()
    print("created customer: {}".format(customer0))
    print("customer.user {}".format(customer0.user))
    print("customer income type: {}".format(customer0.income_type()))

    customer1 = factory.create_customer()
    print("created customer: {}".format(customer1))
    print("customer.user {}".format(customer1.user))
    print("customer income type: {}".format(customer1.income_type()))
