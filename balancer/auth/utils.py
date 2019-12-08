import base64
import binascii
import functools
from http import HTTPStatus
from typing import Callable, Optional, Tuple

import jwt
from flask import request, Response
from jwt import PyJWTError

from balancer.auth.data import Role, SECRET_KEY


def parse_basic_auth(basic_auth: str) -> Optional[Tuple[str, str]]:
    if "Basic" not in basic_auth:
        return None

    pair = basic_auth.split()
    if not len(pair) == 2:
        return None

    credentials_encoded = pair[1]
    try:
        credentials_decoded = base64.urlsafe_b64decode(credentials_encoded).decode()
    except binascii.Error:
        return None

    name_password = credentials_decoded.split(":")
    if not len(name_password) == 2:
        return None

    return name_password


def create_jwt(role: Role) -> str:
    payload = {
        "role": role.value
    }

    token = jwt.encode(
        payload=payload,
        key=SECRET_KEY,
        algorithm="HS256"
    )

    return token.decode()


def parse_role(token: str) -> Optional[Role]:
    try:
        payload = jwt.decode(
            jwt=token,
            key=SECRET_KEY,
            algorithms=["HS256"]
        )
    except PyJWTError:
        return None

    return Role(payload["role"])


class allowed_for:

    def __init__(self, *roles: Tuple[Role]):
        self._roles = set(roles)

    def __call__(self, func: Callable):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            if "Authorization" not in request.headers:
                return Response(status=HTTPStatus.UNAUTHORIZED)

            pair = request.headers["Authorization"].split()
            if not len(pair) == 2:
                return Response(status=HTTPStatus.UNAUTHORIZED)

            token = pair[1]
            role = parse_role(token)

            if role is None or role not in self._roles:
                return Response(status=HTTPStatus.UNAUTHORIZED)

            return func(*args, **kwargs)

        return wrapper
