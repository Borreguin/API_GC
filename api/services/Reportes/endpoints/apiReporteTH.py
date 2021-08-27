import os

import pandas as pd

from api.services.Reportes.endpoints import *
from my_lib.SQLHandler.SQLGestionConocimiento import SQLGestionConocimiento
from my_lib.SQLHandler.Statements import info_personal_basica, funcionarios_direccion
import my_lib.SQLHandler.Keys as Key

ns = api.namespace('reporte-th', description='Relativas a reportes de Talento Humano')


@ns.route('/<string:formato>/informacion-personal')
class InformacionPersonal(Resource):
    @api.response(200, 'El reporte ha sido generado de manera correcta')
    def get(self, formato):
        if not formato in init.allowed_formats:
            return dict(success=False,
                        msg=f"Formato [{formato}] no permitido. Opciones permitidas: {init.allowed_formats}"), 404
        gcServer = SQLGestionConocimiento()
        success_1, df_basic_info, msg = gcServer.execute_as_dataframe(info_personal_basica)
        success_2, df_direccion_info, msg = gcServer.execute_as_dataframe(funcionarios_direccion)
        if not success_1 or not success_2:
            msg = "Error al obtener información básica" if not success_1 else "Error al obtener información de direcciones"
            return dict(success=False, msg=msg), 409
        # Estructurando datos de la tabla resultado:
        to_remove = [Key.per_nombres, Key.per_apellidos]
        df_direccion_info.drop(to_remove, axis=1, inplace=True)
        df_result = pd.merge(df_basic_info, df_direccion_info, on=Key.fun_numero_documento, how="left")
        df_users = gcServer.get_users()


