import requests
from flask import Blueprint, request, jsonify

webhook_bp = Blueprint('webhook', __name__, template_folder='templates')

from . import routes
