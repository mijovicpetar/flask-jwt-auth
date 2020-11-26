"""Ping pong routes."""

from app.hello import hello as h
from app.auth.service import get_current_user
from app.auth.decorators import token_required, admin_role_required, verification_required


@h.route('/')
def hello():
    return {'message': 'Hello.'}

@h.route('/test_token_required')
@token_required
def test_token_required():
    current_user = get_current_user()
    return {
        "message": "Success.",
        "curr_user": current_user.to_dict()
    }

@h.route('/test_admin_role_required')
@token_required
@admin_role_required
def test_admin_role_required():
    current_user = get_current_user()
    return {
        "message": "Success.",
        "curr_user": current_user.to_dict()
    }

@h.route('/test_verification_required')
@token_required
@verification_required
def test_verification_required():
    current_user = get_current_user()
    return {
        "message": "Success.",
        "curr_user": current_user.to_dict()
    }

@h.route('/test_verified_admin_required')
@token_required
@admin_role_required
@verification_required
def test_verified_admin_required():
    current_user = get_current_user()
    return {
        "message": "Success.",
        "curr_user": current_user.to_dict()
    }
