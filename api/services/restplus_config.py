"""
    This file defines all the API's configuration - API Home Page
    Archivo que define la configuración de la API en General - página inicial de la API
    Adds:
        Logger to save all the problems in the API
        Error handler in case is needed
"""
import datetime as dt
from flask_restplus import Api
from settings import initial_settings as init

api = Api(version=init.VERSION, title='API Gestion de Conocimiento Fase 3',
          contact="Roberto Sánchez A, Paulina Vasquez, Michelle Nieto",
          contact_email="rg.sanchez.a@gmail.com, pvasquez@cenace.org.ec, mnieto@cenace.org.ec",
          contact_url="https://github.com/Borreguin",
          description='Esta API despliega los servicios web del proyecto "Gestion de Conocimiento - Fase 3"',
          ordered=False)


# Special JSON encoder for special cases:
def custom_json_encoder(o):
    # this deals with Datetime types:
    if isinstance(o, dt.datetime):
        return o.isoformat()



