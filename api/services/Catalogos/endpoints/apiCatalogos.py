import os
from random import randint
from api.services.Catalogos.endpoints import *
from api.services.Catalogos import serializers as srl
from api.services.Catalogos import parsers
from dto.mongo_classes.catalogos.Ambito import AmbitoFromDataFrame
from my_lib.utils import create_temporal_excel_from_args

ns = api.namespace('catalogo', description='Relativas a la administración de catálogos')

ser_from = srl.Serializers(api)
api = ser_from.add_serializers()


@ns.route('/ambito/from-excel')
@ns.route('/ambito/from-excel/<string:random_key>')
class SRNodeFromExcel(Resource):
    @api.response(200, 'El catálogo ha sido actualizado de manera correcta')
    @api.expect(parsers.excel_upload_w_option)
    def put(self, random_key=None):
        """ Permite actualizar el catálogo Ambito mediante un archivo excel
            DEFAULT:
            Si los registros en cada fila no existen entonces se añaden dentro del catálogo
            REEMPLAZAR:
            El catálogo completo es sustituido de acuerdo a lo especificado en el archivo
        """
        args = parsers.excel_upload.parse_args()
        success, temp_file_path, stream_excel_file = create_temporal_excel_from_args(args, init.TEMP_PATH)
        if not success:
            return dict(success=False, msg="No es posible cargar el archivo"), 409
        success, AmbitoLst, msg = AmbitoFromDataFrame(temp_file_path).get_list()
        # once the file was processed the proceed to delete it
        os.remove(temp_file_path)
        if not success:
            return dict(success=False, msg=msg), 409
        for ambito in AmbitoLst:
            ambito.save()
        return dict(success=True), 200