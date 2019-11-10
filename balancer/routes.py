import requests
import logging
from flask import Response, request

from balancer import config
from . import app, redis


logger = logging.getLogger(__name__)


INDEX_TO_SERVER_URL = {
    0: config.SERVER0_URL,
    1: config.SERVER1_URL
}


def request_server(method: str, key: int) -> Response:
    server_index = key % 2
    server_url = INDEX_TO_SERVER_URL[server_index]

    response = getattr(requests, method)(server_url + f"messages/{key}", data=request.data, headers=request.headers)
    return Response(response=response.text, status=response.status_code, headers=dict(response.headers))


@app.route('/messages/<int:key>', methods=["GET"])
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
def post_message(key: int):
    if redis.exists(key):
        del redis[key]

    return request_server("post", key)


@app.route('/messages/<int:key>', methods=["DELETE"])
def delete_message(key: int):
    if redis.exists(key):
        del redis[key]

    return request_server("delete", key)
