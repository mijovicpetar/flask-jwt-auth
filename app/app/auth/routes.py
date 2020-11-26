"""Auth routes."""

import traceback
from flask import request, Response, redirect, url_for
from flask_cors import cross_origin

from app.auth import authentication as at
from app.auth.models import User
from app.auth.service import AUTH_SERVICE as auth_service
from app.auth.decorators import admin_role_required, token_required
from app.utils.exceptions import ApiException
from app.utils.decorators import handle_api_exception


# @at.route('/api/auth/register/admin', methods=['POST'])
# @cross_origin()
# @handle_api_exception
# def user_register_admin():
#     """Register admin."""
#     return auth_service.register_user(request, role='admin')


@at.route('/api/auth/register', methods=['POST'])
@cross_origin()
@handle_api_exception
def user_register():
    """Register user."""
    return auth_service.register_user(request)


@at.route('/api/auth/login', methods=['POST'])
@cross_origin()
@handle_api_exception
def login_user():
    return auth_service.login_user(request)


@at.route('/api/auth/logout', methods=['POST'])
@cross_origin
@handle_api_exception
def logout_user():
    return auth_service.logout_user()


@at.route('/api/auth/user/verify/<token>')
def confirm_token(token: str):
    try:
        auth_service.confirm_token(token)
    except:
        traceback.print_exc()

    return redirect(url_for('website_server.home'))


@at.route('/api/auth/user/<int:id>', methods=['GET'])
@token_required
@admin_role_required
@handle_api_exception
def get_user_by_id(id: int):
    return auth_service.get_user_by_id(id)


@at.route('/api/auth/my_data')
@token_required
@handle_api_exception
def get_current_user_data():
    return auth_service.get_current_user_data()


@at.route('/api/auth/reset-password', methods=['POST'])
@cross_origin()
@handle_api_exception
def reset_password():
    return auth_service.reset_password(request)

@at.route('/api/auth/admins', methods=['GET'])
@cross_origin()
@handle_api_exception
@token_required
@admin_role_required
def get_all_admins():
    return auth_service.get_all_admins()

@at.route('/api/auth/customers', methods=['GET'])
@cross_origin()
@handle_api_exception
@token_required
@admin_role_required
def get_all_customers():
    return auth_service.get_all_customers()

@at.after_request
def creds(response):
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
