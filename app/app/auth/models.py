"""Auth models."""

from datetime import datetime
from itsdangerous import URLSafeTimedSerializer

from app import DB, BCRYPT


class User(DB.Model):
    """User model."""
    __tablename__ = 'users'
    id = DB.Column(DB.Integer, primary_key=True)
    role = DB.Column(DB.String(50), default='user')
    first_name = DB.Column(DB.String(100))
    last_name = DB.Column(DB.String(100))
    email = DB.Column(DB.String(150), unique=True, index=True)
    password = DB.Column(DB.String(150))
    country = DB.Column(DB.String(150))
    city = DB.Column(DB.String(50))
    phone_number = DB.Column(DB.String(50))
    address = DB.Column(DB.String(90))
    verified = DB.Column(DB.Boolean)

    def __init__(self, role, first_name, last_name, email, password, country, city, phone_number, address, verified):
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.country = country
        self.city = city
        self.phone_number = phone_number
        self.address = address
        self.verified = verified

    def check_password(self, password):
        """Check entered password."""
        return BCRYPT.check_password_hash(self.password, password)

    @classmethod
    def create_user(cls, first_name, last_name, email, password, country, city, phone_number, address, role='user'):
        user = cls(role=role,
                   first_name=first_name,
                   last_name=last_name,
                   email=email,
                   password=BCRYPT.generate_password_hash(password).decode('utf-8'),
                   country=country,
                   city=city,
                   phone_number=phone_number,
                   address=address,
                   verified=False)

        DB.session.add(user)
        DB.session.commit()

        return user

    @classmethod
    def set_password(cls, email:str, raw_password:str):
        """Set user password."""
        user = User.query.filter_by(email=email).first()

        if user:
            password = BCRYPT.generate_password_hash(raw_password).decode('utf-8')
            user.password = password
            DB.session.commit()

        return user

    @classmethod
    def verify_user(cls, email: str):
        """Set user verified to True."""
        user = User.query.filter_by(email=email).first()

        if user:
            user.verified = True
            DB.session.commit()
            return True

        return False

    def load_user(id):
        """Fetch user object."""
        return User.query.get(int(id))

    def to_dict(self):
        """Create dictionary from Product model."""
        my_dict = dict()
        my_dict["id"] = self.id
        my_dict["first_name"] = self.first_name
        my_dict["last_name"] = self.last_name
        my_dict["email"] = self.email
        my_dict["country"] = self.country
        my_dict["city"] = self.city
        my_dict["phone_number"] = self.phone_number
        my_dict["address"] = self.address
        my_dict["verified"] = self.verified
        my_dict["role"] = self.role
        return my_dict
