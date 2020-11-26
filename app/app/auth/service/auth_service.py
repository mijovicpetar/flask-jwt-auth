"""Auth Service"""

import random
import string
import traceback
import jwt

from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer
from flask import current_app, url_for, session

from app.auth.models import User
from app.utils.exceptions import ApiException, BadDataApiException, InternalErrorApiException, API_UNPROCESSABLE_ENTITY
from app.utils.helpers import get_data
from app.utils.services import EmailService


class AuthService():
    """Auth Service"""

    @classmethod
    def _gen_random_string(cls, length=8) -> str:
        """Generate random string.

        Args:
            length (int, optional): [Length]. Defaults to 8.

        Returns:
            [str]: Generated string.
        """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    @classmethod
    def _generate_confirmation_token(cls, email: str) -> str:
        """Generate confirmation token for email address.

        Args:
            email (str): Token is generated for this email.

        Returns:
            str: Confirmation token.
        """
        secret_key = current_app.config['SECRET_KEY']
        password_salt = current_app.config['SECURITY_PASSWORD_SALT']

        serializer = URLSafeTimedSerializer(secret_key)
        return serializer.dumps(email, salt=password_salt)

    @classmethod
    def _send_confirmation_email(cls, recv_email: str, token: str, base_url: str):
        """Send confirmation email.

        Args:
            recv_email (str): Target email address.
            token (str): Confirmation token.
            base_url (str): Server url.

        Raises:
            InternalErrorApiException: If error occures while sending email.
        """
        url = base_url
        url += url_for('authentication.confirm_token', token=token)

        email_sent = EmailService.send_template_email(
            recv_email,
            'Registration confirmation',
            'mail_template_registration.html',
            url)

    @classmethod
    def register_user(cls, request, role='user') -> dict:
        """Register user.

        Args:
            request ([type]): Request.
            role (str, optional): User role. Defaults to 'user'.

        Raises:
            BadDataApiException: If data not as expected or admin not from psoftware.

        Returns:
            dict: User data dict.
        """
        # Extract data from request.
        data_dict = get_data(request)

        name = data_dict.get("first_name")
        last_name = data_dict.get("last_name")
        email = data_dict.get("email")
        password = data_dict.get("password")
        country = data_dict.get("country")
        city = data_dict.get("city")
        phone_number = data_dict.get("phone_number")
        address = data_dict.get("address")

        if role == 'admin' and '@psoftware.co' not in email:
            raise BadDataApiException('Admin domain error.')

        try:
            # Create user in db.
            user = User.create_user(
                name, last_name, email, password, country, city, phone_number,
                address, role=role)
        except:
            raise BadDataApiException('User data not correct.')

        token = cls._generate_confirmation_token(email)
        base_url_splited = request.base_url.split('/')
        base_url = base_url_splited[0] + '//' + base_url_splited[2]
        cls._send_confirmation_email(email, token, base_url)

        # Registration was success.
        return {
            "message": "Registration successfull.",
            "user_info": user.to_dict()
        }

    @classmethod
    def login_user(cls, request) -> dict:
        """Login user.

        Args:
            request ([type]): Flask request.

        Raises:
            ApiException: If credentials are wrong.

        Returns:
            dict: Response dict.
        """
        data_dict = get_data(request)
        email = data_dict['email']
        password = data_dict['password']

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            raise ApiException("Wrong credentials.", API_UNPROCESSABLE_ENTITY)

        token = jwt.encode({
        'sub': user.email,
        'iat':datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=24*60)},
        current_app.config['SECRET_KEY'])

        session["current_user"] = user.id

        # Login was success.
        return {
            "message": "Login successfull.",
            "user_info": user.to_dict(),
            "token": token.decode('UTF-8')
        }

    @classmethod
    def logout_user(cls) -> dict:
        """Logout user.

        Returns:
            dict: Response dict.
        """
        session["current_user"] = None
        return {
            "message": "User log out completed."
        }

    @classmethod
    def confirm_token(cls, token):
        email = None
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt = current_app.config['SECURITY_PASSWORD_SALT']
            )
        except:
            traceback.print_exc()
            raise ApiException('Invalid token.', API_UNPROCESSABLE_ENTITY)

        if not email:
            raise ApiException('Invalid token.', API_UNPROCESSABLE_ENTITY)

        res = User.verify_user(email)
        if not res:
            raise ApiException('Invalid token.', API_UNPROCESSABLE_ENTITY)

    @classmethod
    def get_user_by_id(cls, user_id: int) -> dict:
        """Get user by id.

        Args:
            user_id (int): Id of target user.

        Returns:
            dict: User dict.
        """
        user = User.query.get(user_id)
        if not user:
            raise BadDataApiException("User not found.")

        return user.to_dict()

    @classmethod
    def get_all_admins(cls):
        """Get all admins.

        Returns:
            Array of dicts
        """
        admins = User.query.filter_by(role="admin").all()
        array = []
        for admin in admins:
            array.append(admin.to_dict())
        return array

    @classmethod
    def get_all_customers(cls):
        """Get all customers.

        Returns:
            Array of dicts
        """
        admins = User.query.filter_by(role="user").all()
        array = []
        for admin in admins:
            array.append(admin.to_dict())
        return array

    @classmethod
    def get_current_user_data(cls) -> dict:
        """Get current user data.

        Returns:
            dict: Current user data.
        """
        current_user = get_current_user()
        if current_user is None:
            return None

        return current_user.to_dict()

    @classmethod
    def reset_password(cls, request) -> dict:
        """Reset password.

        Args:
            request ([type]): Flask request.

        Raises:
            BadDataApiException: If required email not passed or user not found.
            InternalErrorApiException: If error while sending email.
        Returns:
            dict: Response with message.
        """
        data_dict = get_data(request)
        email = data_dict.get('email')

        if not email:
            raise BadDataApiException("Email of user not provided.")

        password = cls._gen_random_string()
        user = User.set_password(email, password)

        if not user:
            raise BadDataApiException("User not found.")

        result = EmailService.send_template_email(
            email,
            "Password reset",
            "mail_template_password.html",
            password
        )

        if not result:
            raise InternalErrorApiException('Error while sending email.')

        return {"message": "Password reset successfull."}


def get_current_user():
    user_id = session.get('current_user')
    if user_id is None:
        return None

    user = User.query.get(user_id)
    return user
