from tests import Base
from .factory import Factory
from gradient.models.user import UserModel
import json


class TestCustomerRegistration(Base):
    """
    This class handles testing customer registration
    """

    def test_with_invalid_jwt(self):
        """
        test /customer/register endpoint without required jwt
        """
        # create a non-token
        access_token = "a-non-token"

        # registration request
        res = self.client.post(
            "/customer/register",
            headers=dict(
                authorization="Bearer {}".format(access_token),
                content_type="application/json",
            ),
            data=dict(income=100, dependents=0, marital_status="single"),
        )

        # assert error code
        self.assertTrue(res.status_code >= 400)

    def test_with_valid_jwt(self):
        """
        test /customer/register endpoint with jwt
        """
        # create user
        factory = Factory(self.app, self.db)
        user = factory.create_user()
        access_token = user.generate_access_token()

        # user's access token to make registration request
        res = self.client.post(
            "/customer/register",
            headers=dict(
                authorization="Bearer {}".format(access_token),
                content_type="application/json",
            ),
            data=dict(income=100, dependents=0, marital_status="single"),
        )

        # assert success
        self.assertEqual(res.status_code, 200)

    def test_on_already_registered_user(self):
        """
        test /customer/register endpoint with an user that has
          already registered before
        """
        # create user/customer
        factory = Factory(self.app, self.db)
        user = factory.create_user(email="test_duplicate@mail.com")
        access_token = user.generate_access_token()
        customer = factory.create_customer(user=user)

        # register customer with existing email
        res = self.client.post(
            "/customer/register",
            headers=dict(
                authorization="Bearer {}".format(access_token),
                content_type="application/json",
            ),
            data=dict(income=100, dependents=0, marital_status="single"),
        )

        # assert failure &
        #   message should contain string "already registered"
        self.assertTrue(res.status_code >= 400)
        self.assertIn("already registered", str(res.data))

    def test_with_valid_input_data(self):
        """
        test /customer/register endpoint with invalid input data
        """
        # create user
        factory = Factory(self.app, self.db)
        user = factory.create_user()
        access_token = user.generate_access_token()

        # missing a required field (income in this case)
        invalid_data_0 = dict(dependents=0, marital_status="single")

        # value of marital_status is not one of the accepted values
        invalid_data_1 = dict(income=100, dependents=0, marital_status="malformed")

        invalid_data = [invalid_data_0, invalid_data_1]

        # test all invalid data inputs
        for data in invalid_data:
            res = self.client.post(
                "/customer/register",
                headers=dict(
                    authorization="Bearer {}".format(access_token),
                    content_type="application/json",
                ),
                data=data,
            )

            # always assert error code
            self.assertTrue(res.status_code >= 400)
