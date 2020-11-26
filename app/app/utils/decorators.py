"""Decorators."""

import traceback
from flask import request, Response
from functools import wraps
from app.utils.exceptions import ApiException


def handle_api_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ApiException as exc:
            return Response(exc.message,
                            status=exc.status,
                            mimetype='application/json')
        except:
            traceback.print_exc()
            return Response("Unexpected error occured.",
                            status=500,
                            mimetype='application/json')

    return wrapper

