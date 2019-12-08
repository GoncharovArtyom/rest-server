import logging
from http import HTTPStatus

import requests
from flask import Response, request

from balancer import config
from balancer.auth.data import NAMES_TO_PASSWORDS, NAMES_TO_ROLES, Role
from balancer.auth.utils import create_jwt, parse_basic_auth, allowed_for
from . import app, redis

logger = logging.getLogger(__name__)

INDEX_TO_SERVER_URL = {
    0: config.SERVER0_URL,
    1: config.SERVER1_URL
}


def request_server(method: str, key: int) -> Response:
    server_index = key % len(INDEX_TO_SERVER_URL)
    server_url = INDEX_TO_SERVER_URL[server_index]

    response = getattr(requests, method)(server_url + f"messages/{key}", data=request.data, headers=request.headers)
    return Response(response=response.text, status=response.status_code, headers=dict(response.headers))


@app.route('/messages/<int:key>', methods=["GET"])
@allowed_for(Role.reader, Role.writer, Role.admin)
def get_message(key: int):
    logger.debug("ask  cache for key=%d" % key)
    if redis.exists(key):
        return Response(redis[key].decode(), content_type="application/json")

    logger.warning("no value in cache for key=%d" % key)
    server_response = request_server("get", key)
    if server_response.status_code == 200:
        redis[key] = server_response.data

    return server_response


@app.route('/messages/<int:key>', methods=["POST"])
@allowed_for(Role.writer, Role.admin)
def post_message(key: int):
    if redis.exists(key):
        del redis[key]

    return request_server("post", key)


@app.route('/messages/<int:key>', methods=["DELETE"])
@allowed_for(Role.admin)
def delete_message(key: int):
    if redis.exists(key):
        del redis[key]

    return request_server("delete", key)


@app.route('/auth', methods=["GET"])
def create_token():
    basic_auth = request.headers.get("Authorization")
    if basic_auth is None:
        return Response(status=HTTPStatus.UNAUTHORIZED)

    name_password = parse_basic_auth(basic_auth)

    if name_password is None:
        return Response(status=HTTPStatus.UNAUTHORIZED)

    name, password = name_password
    if name not in NAMES_TO_PASSWORDS or password != NAMES_TO_PASSWORDS[name]:
        return Response(status=HTTPStatus.UNAUTHORIZED)

    jwt = create_jwt(NAMES_TO_ROLES[name])
    return Response(status=HTTPStatus.OK, headers={"Authorization": f"Bearer {jwt}"})
