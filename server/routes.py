import logging
from http import HTTPStatus

from flask import Response, request, jsonify
from werkzeug.exceptions import BadRequest

from . import app, db
from . import model


logger = logging.getLogger(__name__)


@app.route('/messages/<int:key>', methods=["GET"])
def get_message(key: int):
    message = model.Message.query.filter_by(key=key).first()
    if message is None:
        logger.error("GET: no value in database for key=%d" % key)
        return Response(status=HTTPStatus.NOT_FOUND)

    return jsonify(message.value)


@app.route('/messages/<int:key>', methods=["POST"])
def post_message(key: int):
    if request.json is None:
        raise BadRequest

    old_message = model.Message.query.filter_by(key=key).first()
    if old_message is not None:
        db.session.delete(old_message)

    db.session.add(model.Message(key=key, value=request.json))
    db.session.commit()

    if old_message is None:
        return Response(status=HTTPStatus.CREATED)

    return Response(status=HTTPStatus.OK)


@app.route('/messages/<int:key>', methods=["DELETE"])
def delete_message(key: int):
    message = model.Message.query.filter_by(key=key).first()
    if message is None:
        logger.error("DELETE: no value in database for key=%d" % key)
        return Response(status=HTTPStatus.NOT_FOUND)

    db.session.delete(message)
    db.session.commit()

    return Response(status=HTTPStatus.OK)
