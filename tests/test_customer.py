from tests import Base
from .factory import Factory
from gradient.models.user import UserModel
import json


class TestCustomer(Base):
    """
    This class handles testing getting a customer
    """

    def test_with_invalid_jwt(self):
        """
        test /customer/<int:customer_id> endpoint with invalid jwt
        """
        # create customer
        factory = Factory(self.app, self.db)
        user = factory.create_user()
        customer = factory.create_customer(user=user)

        # create an invalid jwt
        access_token = "a-non-token"

        # get
        res = self.client.get(
            "/customer/{}".format(customer.id),
            headers=dict(authorization="Bearer {}".format(access_token)),
        )

        # assert failed
        self.assertTrue(res.status_code >= 400)

    def test_with_invalid_jwt(self):
        """
        test /customer/<int:customer_id> endpoint with valid jwt
        """
        # create customer
        factory = Factory(self.app, self.db)
        user = factory.create_user()
        customer = factory.create_customer(user=user)
        access_token = user.generate_access_token()

        # get
        res = self.client.get(
            "/customer/{}".format(customer.id),
            headers=dict(authorization="Bearer {}".format(access_token))
        )

        # assert success 
        self.assertEqual(res.status_code, 200)
