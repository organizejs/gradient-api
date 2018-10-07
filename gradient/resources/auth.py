from flask_restful import Resource
from flask_jwt_extended import (
  jwt_required, jwt_refresh_token_required, 
  get_jwt_identity, get_raw_jwt,
)
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, use_args, parser
from passlib.hash import pbkdf2_sha256 as sha256
from flask import current_app, session, make_response
import jwt
import requests
import os
from ..models import UserModel


class RedirectAction:
  REGISTER = "register"
  LOGIN = "login"


class RedirectUri:
  REGISTER = "http://jianshentan-ws.eastus.cloudapp.azure.com:8080/google/register/authorized"
  LOGIN = "http://jianshentan-ws.eastus.cloudapp.azure.com:8080/google/login/authorized"


class GoogleRedirect(Resource):

  google_redirect_args = {
    "type": fields.Str(
      required=True,
      validate=validate.OneOf([
        RedirectAction.REGISTER,
        RedirectAction.LOGIN,
      ])
    )
  }

  @use_args(google_redirect_args)
  def get(self, args):
    # set state:
    state = sha256.hash(os.urandom(1024))

    # select uri based on redirect param
    redirect_uri = RedirectUri.REGISTER \
      if args["type"] == RedirectAction.REGISTER \
      else RedirectUri.LOGIN

    # register with google
    r = requests.get(
      "https://accounts.google.com/o/oauth2/v2/auth", 
      params={
        "client_id": current_app.config["GOOGLE_OAUTH_CLIENT_ID"],
        "response_type": "code",
        "scope": "openid email profile",
        "redirect_uri": redirect_uri,
        "state": state,
        "nonce": "1234567-1234567-1234567",
        "access_type": "offline"
      }
    )

    # send consent screen url for user to go to 
    return r.url


class GoogleAuthorized(Resource):

  @staticmethod
  def exchange_code_for_id(code, redirect_uri):
    '''
    steps:
    1. verify state (TODO)
    2. POST request to exchange code for id
    3. verify request was successful
    4. decode returned jwt "id_token"
    5. validate token (TODO)
    6. verify google account is email verified

    returns decoded jwt json
    '''
    # TODO figure out how to verify state
    # if args["state"] != temporary_state_store["state"]:  
    #   return {
    #     "message": "Invalid state parameter"
    #   }, 401

    r = requests.post(
      "https://www.googleapis.com/oauth2/v4/token",
      data={
        "code": code,
        "client_id": current_app.config["GOOGLE_OAUTH_CLIENT_ID"],
        "client_secret": current_app.config["GOOGLE_OAUTH_CLIENT_SECRET"],
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
      }
    )

    # check that request suceeded
    try:
      r.raise_for_status()
    except:
      return r.json(), 404

    res = r.json() # "access_token", "id_token", "expires_in", "token_type", "refresh_token"

    # decode id_token without validation (a jwt)
    jwt_decoded = jwt.decode(res["id_token"], verify=False)

    # TODO: validate token: 
    #   https://developers.google.com/identity/protocols/OpenIDConnect#validatinganidtoken

    # TODO: validate 'nonce'

    # check that google account is email verified
    if not jwt_decoded["email_verified"]:
      return {
        "message": "Google user {} is not email verified.".format(jwt_decoded["email"])
      }, 404

    return jwt_decoded


class GoogleLoginAuthorized(GoogleAuthorized):
   
  google_response_args = {
    "state": fields.Str(required=True),
    "code": fields.Str(required=True)
  }

 
  @use_args(google_response_args)
  def get(self, args):

    # get id_token (jwt) from google
    jwt_decoded = super().exchange_code_for_id(args["code"], RedirectUri.LOGIN)

    # check that user exists
    user = UserModel.get_by_email(jwt_decoded["email"])
    if user is None:
      return {
        "message": "User {} does not exist.".format(jwt_decoded["email"])
      }, 404
  
    # generate jwt tokens
    access_token = user.generate_access_token()
    refresh_token = user.generate_refresh_token()

    # return access/refresh token for client to use
    return {
      "message": "User with email {} is logged in.".format(user.email),
      "access_token": access_token,
      "refresh_token": refresh_token
    }, 200


class GoogleRegisterAuthorized(GoogleAuthorized):
   
  google_response_args = {
    "state": fields.Str(required=True),
    "code": fields.Str(required=True),
  }


  @use_args(google_response_args)
  def get(self, args):

    # get id_token (jwt from google
    jwt_decoded = super().exchange_code_for_id(args["code"], RedirectUri.REGISTER)
   
    # check that user does not exists
    user = UserModel.get_by_email(jwt_decoded["email"])
    if user:
      return {
        "message": "User {} already exists.".format(jwt_decoded["email"])
      }, 404

    # create user & save to db
    user = UserModel(
      jwt_decoded["email"], 
      jwt_decoded["given_name"], 
      jwt_decoded["family_name"]
    )
    user.save()

    # generate jwt tokens
    access_token = user.generate_access_token()
    refresh_token = user.generate_refresh_token()

    # return access/refresh token for client to use
    return {
      "message": "User with email {} was created.".format(user.email),
      "access_token": access_token,
      "refresh_token": refresh_token
    }, 201


