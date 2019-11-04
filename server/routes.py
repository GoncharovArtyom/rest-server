import functools
from http import HTTPStatus

from flask import Response, request, jsonify
from werkzeug.exceptions import BadRequest

from . import app, db
from . import model
from . config import PATH_TO_LOG_FILE


def log_request(handler):
    @functools.wraps(handler)
    def wrapper(*args, **kwargs):
        with open(PATH_TO_LOG_FILE, "a") as f:
            f.write(f"{request.method} : {request.path} : {request.data}\n")

        return handler(*args, **kwargs)

    return wrapper


@app.route('/messages/<int:key>', methods=["GET"])
@log_request
def get_message(key: int):
    message = model.Message.query.filter_by(key=key).first()
    if message is None:
        return Response(status=HTTPStatus.NOT_FOUND)

    return jsonify(message.value)


@app.route('/messages/<int:key>', methods=["POST"])
@log_request
def post_message(key: int):
    if request.json is None:
        raise BadRequest

    created = model.Message.query.filter_by(key=key).first() is not None
    db.session.add(model.Message(key=key, value=request.json))
    db.session.commit()

    if created:
        return Response(status=HTTPStatus.CREATED)

    return Response(status=HTTPStatus.OK)


@app.route('/messages/<int:key>', methods=["DELETE"])
@log_request
def delete_message(key: int):
    message = model.Message.query.filter_by(key=key).first()
    if message is None:
        return Response(status=HTTPStatus.NOT_FOUND)

    db.session.delete(message)
    db.session.commit()

    return Response(status=HTTPStatus.OK)
