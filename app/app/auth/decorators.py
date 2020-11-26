"""Decorators."""

import traceback
import jwt

from functools import wraps
from flask import Response, abort, request, current_app
from app.auth.models import User
from app.auth.service import get_current_user


def admin_role_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = get_current_user()
        if current_user.role != 'admin':
            abort(401)
        return func(*args, **kwargs)

    return wrapper

def verification_required(func):
    @wraps(func)
    def verification(*args, **kwargs):
        current_user = get_current_user()
        if current_user.verified != True:
            abort(401)
        return func(*args, **kwargs)

    return verification

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        if len(auth_headers) != 2:
            abort(401)

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = User.query.filter_by(email=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')

            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            print('Token expired.')
            abort(401)
        except (jwt.InvalidTokenError, Exception) as exc:
            print(exc)
            abort(401)

    return _verify
