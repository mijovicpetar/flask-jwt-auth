from flask import Blueprint

utils = Blueprint('utils', __name__, template_folder="templates")

from app.utils import exceptions
from app.utils import helpers
from app.utils import services
from app.utils.validators import DataValidator
DATA_VALIDATOR = DataValidator()
