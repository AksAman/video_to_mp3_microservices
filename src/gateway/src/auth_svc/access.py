"""
Communicates with the auth microservice to handle user authentication.
"""
import logging
from typing import Dict, Optional, Tuple
from flask import Request
from decouple import config
import requests

AUTH_SERVICE_ADDRESS = config("AUTH_SERVICE_ADDRESS")
auth_service_api_route = "/auth/api/v1"


def login(request: Request) -> Tuple[Optional[Dict], Optional[Tuple[str, int]]]:
    """
    Wrapper for the login endpoint of the auth microservice.
    """
    auth = request.authorization
    if not auth:
        return None, ("missing authorization header", 401)

    if not auth.username or not auth.password:
        return None, ("missing username or password", 401)

    basicAuth = (auth.username, auth.password)

    auth_service_response = requests.post(
        url=AUTH_SERVICE_ADDRESS + f"{auth_service_api_route}/login",
        auth=basicAuth,
    )

    if auth_service_response.status_code != 200:
        logging.info(f"{auth_service_response.status_code=} {auth_service_response.json()=}")
        return None, ("invalid username or password", auth_service_response.status_code)

    return auth_service_response.json(), None


def validate_token(request: Request) -> Tuple[Optional[Dict], Optional[Tuple[str, int]]]:
    """
    Wrapper for the validate endpoint of the auth microservice.
    ###
    # @name validate_token
    POST {{base_endpoint}}{{auth_api_route}}/validate-token
    Content-Type: {{contentType}}
    Authorization: Bearer {{login.response.body.access}}
    """

    if not "Authorization" in request.headers:
        return {"error": "missing Authorization header"}, 401

    auth_header = request.headers.get("Authorization")
    try:
        auth_type, auth_info = auth_header.split(None, 1)
        auth_type = auth_type.lower()
    except ValueError:
        return {"error": "missing token"}, 400

    if auth_type != "bearer":
        return {"error": "invalid token type"}, 400

    auth_service_response = requests.post(
        url=AUTH_SERVICE_ADDRESS + f"{auth_service_api_route}/validate-token",
        headers={"Authorization": auth_header},
    )

    if auth_service_response.status_code != 200:
        logging.error(auth_service_response.json())
        return None, ("invalid token", auth_service_response.status_code)

    return auth_service_response.json(), 200
