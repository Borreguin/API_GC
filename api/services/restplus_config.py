"""
    This file defines all the API's configuration - API Home Page
    Archivo que define la configuración de la API en General - página inicial de la API
    Adds:
        Logger to save all the problems in the API
        Error handler in case is needed
"""
import json
import traceback
from flask import request
import datetime as dt
from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound
from settings.initial_settings import LogDefaultConfig
from settings import initial_settings as init

""" DB config"""
# dup_key_error = "duplicate key error"
import re


api_log = LogDefaultConfig("api_services.log").logger

api = Api(version=init.VERSION, title='API Gestion de Conocimiento Fase 2',
          contact="Roberto Sánchez A, Paulina Vasquez, Michelle Nieto",
          contact_email="rg.sanchez.a@gmail.com, pvasquez@cenace.org.ec, mnieto@cenace.org.ec",
          contact_url="https://github.com/Borreguin",
          description='Esta API despliega los servicios web del proyecto "Gestion de Conocimiento - Fase 2"',
          ordered=False)


# Special JSON encoder for special cases:
def custom_json_encoder(o):
    # this deals with Datetime types:
    if isinstance(o, dt.datetime):
        return o.isoformat()


@api.errorhandler(Exception)
def default_error_handler(e):
    global api_log
    ts = dt.datetime.now().strftime('[%Y-%b-%d %H:%M:%S.%f]')
    msg = f"{ts} {request.remote_addr} {request.method} {request.scheme}" \
          f"{request.full_path}"
    api_log.error(msg)
    api_log.error(traceback.format_exc())
    if hasattr(e, 'data'):
        return dict(success=False, msg=str(e.data["errors"])), 400

    return dict(success=False, msg=str(e)), 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    api_log.warning(traceback.format_exc())
    return {'message': 'No se obtuvo resultado'}, 404
