from flask import request
from flask_restful import Resource
from ..models import UserModel, CustomerModel, CustomerSchema, MaritalStatus
from webargs import fields, validate
from webargs.flaskparser import use_args, parser
import jwt
from flask_jwt_extended import (
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
)


class Customer(Resource):
    """
    This class handles getting a customer.
    """

    @jwt_required
    def get(self, customer_id):
        customer = CustomerModel.get(customer_id)
        customer_data = CustomerSchema().dump(customer).data
        return customer_data, 200


class CustomerRegister(Resource):
    """
    This class handles customer registration.
    """

    registration_args = {
        "income": fields.Int(required=True),
        "dependents": fields.Int(required=True),
        "marital_status": fields.Str(
            required=True, validate=validate.OneOf([e.value for e in MaritalStatus])
        ),
    }

    @use_args(registration_args)
    @jwt_required
    def post(self, args):
        """
        handles request to register as a customer
        """
        # get user from jwt
        current_user_email = get_jwt_identity()
        current_user = UserModel.get_by_email(current_user_email)

        # check that no customer with associated user already exists
        if current_user.customer is not None:
            return (
                {
                    "message": "This user {} is already registered.".format(
                        current_user.email
                    )
                },
                404,
            )

        # create customer
        customer = CustomerModel(
            user=current_user,
            income=args["income"],
            dependents=args["dependents"],
            marital_status=MaritalStatus(args["marital_status"]),
        )
        customer.save()

        # deserialized customer
        customer_data = CustomerSchema().dump(customer).data

        return customer_data, 200
