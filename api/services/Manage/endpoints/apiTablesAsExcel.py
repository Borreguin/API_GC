import os
from random import randint
from api.services.Manage.endpoints import *
from api.services.Manage import serializers as srl
from api.services.Manage import parsers
from dto.mongo_classes.tablas.CompetenciaConductual import CompetenciaConductualAsDataFrame, CompetenciaConductual
from dto.mongo_classes.tablas.CompetenciaTecnica import CompetenciaTecnicaAsDataFrame, CompetenciaTecnica
from my_lib.utils import create_temporal_excel_from_args, update_or_replace_registers, save_excel_file_from_bytes

ns = api.namespace('tables-as-excel', description='Relativas a la administración de tablas')

ser_from = srl.Serializers(api)
api = ser_from.add_serializers()


@ns.route('/competencia-conductual')
class CompetenciaConductualFromExcel(Resource):
    @api.response(200, 'El catálogo ha sido actualizado de manera correcta')
    @api.expect(parsers.excel_upload_w_option)
    def put(self):
        """ Permite actualizar el catálogo CompetenciaConductual mediante un archivo excel
            DEFAULT (sin valor):
            Si los registros en cada fila no existen entonces se añaden dentro del catálogo
            REEMPLAZAR:
            El catálogo completo es sustituido de acuerdo a lo especificado en el archivo
        """
        args = parsers.excel_upload.parse_args()
        filename = args['excel_file'].filename
        success, temp_file_path, stream_excel_file = create_temporal_excel_from_args(args, init.TEMP_PATH)
        if not success:
            return dict(success=False, msg="No es posible cargar el archivo"), 409
        success, CompetenciaConductualLst, msg = CompetenciaConductualAsDataFrame(temp_file_path).get_object_list_from_excel()
        # once the file was processed, one proceeds to delete it
        os.remove(temp_file_path)
        if not success:
            return dict(success=False, msg=msg), 409
        option = str(args['option']).upper() if args['option'] is not None else "EDITAR"
        success, msg = update_or_replace_registers(CompetenciaConductual, CompetenciaConductualLst, option)
        destination = os.path.join(init.EXCEL_REPO, filename)
        save_excel_file_from_bytes(destination=destination, stream_excel_file=stream_excel_file)
        return dict(success=success, msg=msg), 200 if success else 409

    def get(self):
        """
            Permite descargar la última versión en formato Excel de este catálogo
        """
        file_name = f"CompetenciaConductual.xlsx"
        file_path = os.path.join(init.TEMP_PATH, file_name)
        success, msg = CompetenciaConductualAsDataFrame().get_excel_from_db(file_path)
        if success:
            return send_from_directory(os.path.dirname(file_path), file_name, as_attachment=True)
        else:
            return dict(success=False, msg=msg), 404

@ns.route('/competencia-tecnica')
class CompetenciaTecnicaFromExcel(Resource):
    @api.response(200, 'El catálogo ha sido actualizado de manera correcta')
    @api.expect(parsers.excel_upload_w_option)
    def put(self):
        """ Permite actualizar el catálogo CompetenciaTecnica mediante un archivo excel
            DEFAULT (sin valor):
            Si los registros en cada fila no existen entonces se añaden dentro del catálogo
            REEMPLAZAR:
            El catálogo completo es sustituido de acuerdo a lo especificado en el archivo
        """
        args = parsers.excel_upload.parse_args()
        filename = args['excel_file'].filename
        success, temp_file_path, stream_excel_file = create_temporal_excel_from_args(args, init.TEMP_PATH)
        if not success:
            return dict(success=False, msg="No es posible cargar el archivo"), 409
        success, CompetenciaTecnicaLst, msg = CompetenciaTecnicaAsDataFrame(temp_file_path).get_object_list_from_excel()
        # once the file was processed, one proceeds to delete it
        os.remove(temp_file_path)
        if not success:
            return dict(success=False, msg=msg), 409
        option = str(args['option']).upper() if args['option'] is not None else "EDITAR"
        success, msg = update_or_replace_registers(CompetenciaTecnica, CompetenciaTecnicaLst, option)
        destination = os.path.join(init.EXCEL_REPO, filename)
        save_excel_file_from_bytes(destination=destination, stream_excel_file=stream_excel_file)
        return dict(success=success, msg=msg), 200 if success else 409

    def get(self):
        """
            Permite descargar la última versión en formato Excel de este catálogo
        """
        file_name = f"CompetenciaTecnica.xlsx"
        file_path = os.path.join(init.TEMP_PATH, file_name)
        success, msg = CompetenciaTecnicaAsDataFrame().get_excel_from_db(file_path)
        if success:
            return send_from_directory(os.path.dirname(file_path), file_name, as_attachment=True)
        else:
            return dict(success=False, msg=msg), 404



