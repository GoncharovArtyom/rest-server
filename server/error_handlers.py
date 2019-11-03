import sys
import traceback
from http import HTTPStatus

from flask import Response
from werkzeug.exceptions import HTTPException

from . import app


@app.errorhandler(HTTPException)
def handler(error: HTTPException):
    return Response(status=error.code)


@app.errorhandler(Exception)
def handler(error: Exception):
    traceback.print_exc(file=sys.stdout)
    return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
