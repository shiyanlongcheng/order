from flask import Blueprint

route_api = Blueprint('api_pages', __name__)
from web.controllers.api.Member import *
from web.controllers.api.Address import *
from web.controllers.api.express import *
from web.controllers.api.Takeout import *
from web.controllers.api.Help import *
from web.controllers.api.Second import *
from web.controllers.api.commonweal import *
from web.controllers.api.Person import *


@route_api.route("/")
def index():
    return "Nima api V1.0"
