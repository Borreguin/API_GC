from flask_restplus import Resource
from flask import request, send_from_directory
from settings import initial_settings as init
from api.services.restplus_config import api

# configurando logger y el servicio web
log = init.LogDefaultConfig("ws_catalogos.log").logger