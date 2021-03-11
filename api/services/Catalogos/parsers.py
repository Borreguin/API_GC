from flask_restplus import reqparse
from my_lib import utils as u
import werkzeug
from settings.initial_settings import SUPPORTED_FORMAT_DATES as fmt_time_list
from settings.initial_settings import DEFAULT_DATE_FORMAT as fmt_time_default
import datetime as dt
"""
    Configure the API HTML to show for each services the arguments that are needed 
    (Explain the arguments for each service)
    Cada Parse indica como se deben obervar los modelos desde afuera, explicación 
    de la API en su página inicial
"""

excel_upload = reqparse.RequestParser()
excel_upload.add_argument('excel_file',
                         type=werkzeug.datastructures.FileStorage,
                         location='files',
                         required=True,
                         help='xls, xlsx file')
excel_upload_w_option = excel_upload
excel_upload_w_option.add_argument('option', type=str, required=False, help="'REEMPLAZAR' para sustituir")

file_upload = reqparse.RequestParser()
file_upload.add_argument('file',
                         type=werkzeug.datastructures.FileStorage,
                         location='files',
                         required=True,
                         help='xls, xlsx file')
