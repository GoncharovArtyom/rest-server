import functools
from http import HTTPStatus

from flask import Response, request

from . import app, REDIS, PATH_TO_LOG_FILE


def log_request(handler):
    @functools.wraps(handler)
    def wrapper(*args, **kwargs):
        with open(PATH_TO_LOG_FILE, "a") as f:
            f.write(f"{request.path}: {request.data}\n")

        return handler(*args, **kwargs)

    return wrapper


@app.route('/messages/<int:key>', methods=["GET"])
@log_request
def get_message(key: int):
    if REDIS.exists(key):
        return Response(REDIS[key], status=HTTPStatus.OK)

    return Response(status=HTTPStatus.NOT_FOUND)


@app.route('/messages/<int:key>', methods=["POST"])
@log_request
def post_message(key: int):
    created = not REDIS.exists(key)
    REDIS[key] = request.data

    if created:
        return Response(status=HTTPStatus.CREATED)

    return Response(status=HTTPStatus.OK)


@app.route('/messages/<int:key>', methods=["DELETE"])
@log_request
def delete_message(key: int):
    if REDIS.exists(key):
        del REDIS[key]
        return Response(status=HTTPStatus.OK)

    return Response(status=HTTPStatus.NOT_FOUND)
