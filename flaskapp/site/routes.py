from flask import Blueprint

site = Blueprint('site', __name__)


@site.route('/')
def home():
    return '<h1> Welcome to our Chicago 311 Service </h1>'
