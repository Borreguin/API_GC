from flask_restplus import Resource
from flask import request, send_from_directory
from settings import initial_settings as init
from api.services.restplus_config import api
from dto.mongo_classes.catalogos.Ambito import AmbitoAsDataFrame, Ambito
from dto.mongo_classes.catalogos.ConocimientoInstitucional import ConocimientoInstitucionalAsDataFrame, \
    ConocimientoInstitucional
from dto.mongo_classes.catalogos.InstitucionExterna import InstitucionExternaAsDataFrame, InstitucionExterna
from dto.mongo_classes.catalogos.Mision import MisionAsDataFrame, Mision
from dto.mongo_classes.catalogos.PuestoFuncionario import PuestoFuncionarioAsDataFrame, PuestoFuncionario
from dto.mongo_classes.catalogos.RelacionInterna import RelacionInterna, RelacionInternaAsDataFrame
from dto.mongo_classes.catalogos.UnidadAdministrativa import UnidadAdministrativaAsDataFrame, UnidadAdministrativa


# configurando logger y el servicio web
log = init.LogDefaultConfig("ws_catalogos_tablas.log").logger