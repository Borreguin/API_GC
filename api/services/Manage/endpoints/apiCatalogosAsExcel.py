import os
from random import randint
from api.services.Manage.endpoints import *
from api.services.Manage import serializers as srl
from api.services.Manage import parsers
from my_lib.utils import create_temporal_excel_from_args, update_or_replace_registers, save_excel_file_from_bytes

ns = api.namespace('catalogo-as-excel', description='Relativas a la administración de catálogos')

ser_from = srl.Serializers(api)
api = ser_from.add_serializers()


@ns.route('/ambito')
class AmbitoFromExcel(Resource):
    @api.response(200, 'El catálogo ha sido actualizado de manera correcta')
    @api.expect(parsers.excel_upload_w_option)
    def put(self):
        """ Permite actualizar el catálogo Ambito mediante un archivo excel
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
        success, AmbitoLst, msg = AmbitoAsDataFrame(temp_file_path).get_object_list_from_excel()
        # once the file was processed, one proceeds to delete it
        os.remove(temp_file_path)
        if not success:
            return dict(success=False, msg=msg), 409
        option = str(args['option']).upper() if args['option'] is not None else "EDITAR"
        success, msg = update_or_replace_registers(Ambito, AmbitoLst, option)
        destination = os.path.join(init.EXCEL_REPO, filename)
        save_excel_file_from_bytes(destination=destination, stream_excel_file=stream_excel_file)
        return dict(success=success, msg=msg), 200 if success else 409

    def get(self):
        """
            Permite descargar la última versión en formato Excel de este catálogo
        """
        file_name = f"Ambito.xlsx"
        file_path = os.path.join(init.TEMP_PATH, file_name)
        success, msg = AmbitoAsDataFrame().get_excel_from_db(file_path)
        if success:
            return send_from_directory(os.path.dirname(file_path), file_name, as_attachment=True)
        else:
            return dict(success=False, msg=msg), 500


@ns.route('/conocimiento-institucional')
class ConocimientoFromExcel(Resource):
    @api.response(200, 'El catálogo ha sido actualizado de manera correcta')
    @api.expect(parsers.excel_upload_w_option)
    def put(self):
        """ Permite actualizar el catálogo ConocimientoInstitucional mediante un archivo excel
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
        success, ConocimientoInstitucionalLst, msg = ConocimientoInstitucionalAsDataFrame(
            temp_file_path).get_object_list_from_excel()
        # once the file was processed, one proceeds to delete it
        os.remove(temp_file_path)
        if not success:
            return dict(success=False, msg=msg), 409
        option = str(args['option']).upper() if args['option'] is not None else "EDITAR"
        success, msg = update_or_replace_registers(ConocimientoInstitucional, ConocimientoInstitucionalLst, option)
        destination = os.path.join(init.EXCEL_REPO, filename)
        save_excel_file_from_bytes(destination=destination, stream_excel_file=stream_excel_file)
        return dict(success=success, msg=msg), 200 if success else 409

    def get(self):
        """
            Permite descargar la última versión en formato Excel de este catálogo
        """
        file_name = f"ConocimientoInstitucional.xlsx"
        file_path = os.path.join(init.TEMP_PATH, file_name)
        success, msg = ConocimientoInstitucionalAsDataFrame().get_excel_from_db(file_path)
        if success:
            return send_from_directory(os.path.dirname(file_path), file_name, as_attachment=True)
        else:
            return dict(success=False, msg=msg), 500


@ns.route('/institucion-externa')
class InstitucionesExternasFromExcel(Resource):
    @api.response(200, 'El catálogo ha sido actualizado de manera correcta')
    @api.expect(parsers.excel_upload_w_option)
    def put(self):
        """ Permite actualizar el catálogo InstitucionExterna mediante un archivo excel
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
        success, InstitucionesExternasLst, msg = InstitucionExternaAsDataFrame(
            temp_file_path).get_object_list_from_excel()
        # once the file was processed, one proceeds to delete it
        os.remove(temp_file_path)
        if not success:
            return dict(success=False, msg=msg), 409
        option = str(args['option']).upper() if args['option'] is not None else "EDITAR"
        success, msg = update_or_replace_registers(InstitucionExterna, InstitucionesExternasLst, option)
        destination = os.path.join(init.EXCEL_REPO, filename)
        save_excel_file_from_bytes(destination=destination, stream_excel_file=stream_excel_file)
        return dict(success=success, msg=msg), 200 if success else 409

    def get(self):
        """
            Permite descargar la última versión en formato Excel de este catálogo
        """
        file_name = f"InstitucionExterna.xlsx"
        file_path = os.path.join(init.TEMP_PATH, file_name)
        success, msg = InstitucionExternaAsDataFrame().get_excel_from_db(file_path)
        if success:
            return send_from_directory(os.path.dirname(file_path), file_name, as_attachment=True)
        else:
            return dict(success=False, msg=msg), 500


@ns.route('/mision')
class MisionFromExcel(Resource):
    @api.response(200, 'El catálogo ha sido actualizado de manera correcta')
    @api.expect(parsers.excel_upload_w_option)
    def put(self):
        """ Permite actualizar el catálogo Mision mediante un archivo excel
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
        success, MisionLst, msg = MisionAsDataFrame(temp_file_path).get_object_list_from_excel()
        # once the file was processed, one proceeds to delete it
        os.remove(temp_file_path)
        if not success:
            return dict(success=False, msg=msg), 409
        option = str(args['option']).upper() if args['option'] is not None else "EDITAR"
        success, msg = update_or_replace_registers(Mision, MisionLst, option)
        destination = os.path.join(init.EXCEL_REPO, filename)
        save_excel_file_from_bytes(destination=destination, stream_excel_file=stream_excel_file)
        return dict(success=success, msg=msg), 200 if success else 409

    def get(self):
        """
            Permite descargar la última versión en formato Excel de este catálogo
        """
        file_name = f"Mision.xlsx"
        file_path = os.path.join(init.TEMP_PATH, file_name)
        success, msg = MisionAsDataFrame().get_excel_from_db(file_path)
        if success:
            return send_from_directory(os.path.dirname(file_path), file_name, as_attachment=True)
        else:
            return dict(success=False, msg=msg), 500


@ns.route('/puesto-funcionario')
class PuestoFuncionarioFromExcel(Resource):
    @api.response(200, 'El catálogo ha sido actualizado de manera correcta')
    @api.expect(parsers.excel_upload_w_option)
    def put(self):
        """ Permite actualizar el catálogo PuestoFuncionario mediante un archivo excel
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
        success, PuestoFuncionarioLst, msg = PuestoFuncionarioAsDataFrame(temp_file_path).get_object_list_from_excel()
        # once the file was processed, one proceeds to delete it
        os.remove(temp_file_path)
        if not success:
            return dict(success=False, msg=msg), 409
        option = str(args['option']).upper() if args['option'] is not None else "EDITAR"
        success, msg = update_or_replace_registers(PuestoFuncionario, PuestoFuncionarioLst, option)
        destination = os.path.join(init.EXCEL_REPO, filename)
        save_excel_file_from_bytes(destination=destination, stream_excel_file=stream_excel_file)
        return dict(success=success, msg=msg), 200 if success else 409

    def get(self):
        """
            Permite descargar la última versión en formato Excel de este catálogo
        """
        file_name = f"PuestoFuncionario.xlsx"
        file_path = os.path.join(init.TEMP_PATH, file_name)
        success, msg = PuestoFuncionarioAsDataFrame().get_excel_from_db(file_path)
        if success:
            return send_from_directory(os.path.dirname(file_path), file_name, as_attachment=True)
        else:
            return dict(success=False, msg=msg), 500


@ns.route('/relacion-interna')
class RelacionesInternasFromExcel(Resource):
    @api.response(200, 'El catálogo ha sido actualizado de manera correcta')
    @api.expect(parsers.excel_upload_w_option)
    def put(self):
        """ Permite actualizar el catálogo RelacionInterna mediante un archivo excel
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
        success, RelacionesInternasLst, msg = RelacionInternaAsDataFrame(temp_file_path).get_object_list_from_excel()
        # once the file was processed, one proceeds to delete it
        os.remove(temp_file_path)
        if not success:
            return dict(success=False, msg=msg), 409
        option = str(args['option']).upper() if args['option'] is not None else "EDITAR"
        success, msg = update_or_replace_registers(RelacionInterna, RelacionesInternasLst, option)
        destination = os.path.join(init.EXCEL_REPO, filename)
        save_excel_file_from_bytes(destination=destination, stream_excel_file=stream_excel_file)
        return dict(success=success, msg=msg), 200 if success else 409

    def get(self):
        """
            Permite descargar la última versión en formato Excel de este catálogo
        """
        file_name = f"RelacionInterna.xlsx"
        file_path = os.path.join(init.TEMP_PATH, file_name)
        success, msg = RelacionInternaAsDataFrame().get_excel_from_db(file_path)
        if success:
            return send_from_directory(os.path.dirname(file_path), file_name, as_attachment=True)
        else:
            return dict(success=False, msg=msg), 500


@ns.route('/unidad-administrativa')
class UnidadAdministrativaFromExcel(Resource):
    @api.response(200, 'El catálogo ha sido actualizado de manera correcta')
    @api.expect(parsers.excel_upload_w_option)
    def put(self):
        """ Permite actualizar el catálogo UnidadAdministrativa mediante un archivo excel
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
        success, UnidadAdministrativaLst, msg = UnidadAdministrativaAsDataFrame(
            temp_file_path).get_object_list_from_excel()
        # once the file was processed, one proceeds to delete it
        os.remove(temp_file_path)
        if not success:
            return dict(success=False, msg=msg), 409
        option = str(args['option']).upper() if args['option'] is not None else "EDITAR"
        success, msg = update_or_replace_registers(UnidadAdministrativa, UnidadAdministrativaLst, option)
        destination = os.path.join(init.EXCEL_REPO, filename)
        save_excel_file_from_bytes(destination=destination, stream_excel_file=stream_excel_file)
        return dict(success=success, msg=msg), 200 if success else 409

    def get(self):
        """
            Permite descargar la última versión en formato Excel de este catálogo
        """
        file_name = f"UnidadAdministrativa.xlsx"
        file_path = os.path.join(init.TEMP_PATH, file_name)
        success, msg = UnidadAdministrativaAsDataFrame().get_excel_from_db(file_path)
        if success:
            return send_from_directory(os.path.dirname(file_path), file_name, as_attachment=True)
        else:
            return dict(success=False, msg=msg), 500
