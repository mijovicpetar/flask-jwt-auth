"""Ping pong module."""

from flask import Blueprint

hello = Blueprint('hello', __name__, template_folder="templates")

from app.hello import routes
