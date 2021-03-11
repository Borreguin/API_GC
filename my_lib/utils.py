import argparse, os
import datetime as dt
import hashlib
import json
import traceback
from random import randint
import pandas as pd
import pickle as pkl

script_path = os.path.dirname(os.path.abspath(__file__))


def valid_date(s):
    try:
        return dt.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "El parámetro: '{0}' no es una fecha válida, (formato YYYY-MM-DD).".format(s)
        raise argparse.ArgumentTypeError(msg)


def get_dates_for_last_month():
    d_n = dt.datetime.now()
    date_ini = dt.datetime(year=d_n.year, month=d_n.month - 1, day=1)
    date_end = dt.datetime(year=d_n.year, month=d_n.month, day=d_n.day) - dt.timedelta(days=d_n.day)
    return date_ini, date_end


def check_date_yyyy_mm_dd(s):
    try:
        return True, dt.datetime.strptime(s, "%Y-%m-%d")
    except Exception as e:
        return False, str(e)


def check_date_yyyy_mm_dd_hh_mm_ss(s):
    try:
        return True, dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return False, str(e)


def read_excel(file_name):
    """
    Lee un archivo excel y devuelve un diccionario de DataFrames
    :param file_name: path del archivo a leer
    :return: diccionario de DataFrames
    """
    # variables generales usadas en el script:
    name = file_name.split('\\')
    name = name[-1]
    file_time = None
    last_time = -1
    df_update = pd.DataFrame(columns=["time"])

    # configurando rutas:
    db_path = script_path.replace("my_lib", "_db")
    pkl_file = os.path.join(db_path, name.replace("xlsx", "pkl"))
    json_file = os.path.join(db_path, "update_time.json")

    # verificando si los archivos existen:
    json_exists = os.path.exists(json_file)
    file_exists = os.path.exists(file_name)
    pkl_exists = os.path.exists(pkl_file)

    if file_exists:
        # obtener la hora de última modificación
        file_time = os.path.getmtime(file_name)
    else:
        msg = "El archivo {0} no existe".format(file_name)
        print(msg)
        return None, msg

    # si el archivo json existe, obtener last_time
    if json_exists:
        df_update = pd.read_json(json_file)
        if name in df_update.index:
            last_time = df_update["time"][name]

    # grabar file_time in df_update:
    df_update.loc[name] = [file_time]
    df_update.to_json(json_file)

    # si hay una modificación en el archivo Excel, leer el archivo
    # y transformarlo en formato pkl
    if last_time != file_time or not pkl_exists:
        try:
            xls = pd.ExcelFile(file_name)
            dt_excel = dict()
            for s in xls.sheet_names:
                dt_excel[s] = pd.read_excel(xls, s)
            with open(pkl_file, 'wb') as handle:
                pkl.dump(dt_excel, handle, protocol=pkl.HIGHEST_PROTOCOL)
            return dt_excel, "[{0}] Leído correctamente".format(file_name)
        except Exception as e:
            return None, str(e)
    elif pkl_exists and last_time == file_time:
        with open(pkl_file, 'rb') as handle:
            dt_excel = pkl.load(handle)
        return dt_excel, "[{0}] Leído correctamente".format(file_name)


def group_files(repo, files):
    # let´s group files with similar name
    to_work = [os.path.splitext(f)[0] for f in files]
    groups = sorted(list(set([n.split("@")[0] for n in to_work])))
    done_list = list()
    result = dict()
    for ix, group in enumerate(to_work):
        if group in groups and to_work.index(group) not in done_list:
            result[group] = [files[to_work.index(group)]]
            done_list.append(to_work.index(group))
        else:
            continue
        rest_list = [i for i in range(len(to_work)) if i not in done_list]
        for iy in rest_list:
            if group in to_work[iy] or to_work[iy] in group:
                done_list.append(iy)
                result[group].append(files[iy])

    rest_list = [i for i in range(len(to_work)) if i not in done_list]
    if len(rest_list) > 0:
        for r in rest_list:
            result[files[r]] = [files[r]]
    final = dict()
    for k in sorted(result.keys()):
        final[k] = [dict(name=file,
                         datetime=str(dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(repo, file)))))
                    for file in result[k]]

    return final


def get_id(params: list):
    id = str()
    for p in params:
        id += str(p).lower().strip()
    return hashlib.md5(id.encode()).hexdigest()


def retrieve_from_file(temp_file, id):
    if os.path.exists(temp_file):
        with open(temp_file) as json_file:
            resp = json.load(json_file)
            size = os.path.getsize(temp_file)
            if size > 10 * 1024 * 1024:
                os.remove(temp_file)
            return resp.pop(id, None)
    else:
        return None


def save_in_file(temp_file, id, data_dict):
    if not os.path.exists(temp_file):
        to_save = {id: data_dict}
    else:
        with open(temp_file) as json_file:
            to_save = json.load(json_file)
            to_save.update({id: data_dict})

    with open(temp_file, 'w') as outfile:
        json.dump(to_save, outfile, indent=4, sort_keys=True)


def is_active(path_file, id: str, time_delta: dt.timedelta):
    try:
        value_dict = retrieve_from_file(path_file, id)
        if value_dict is None:
            return False
        else:
            value_dict["fecha"] = dt.datetime.strptime(value_dict["fecha"], "%Y-%m-%d %H:%M:%S")
            if value_dict["fecha"] + time_delta > dt.datetime.now():
                return value_dict["activo"]
            else:
                return False

    except Exception as e:
        tb = traceback.extract_stack()
        print(f"{str(e)} \n {tb}")
        return True


def get_df_from_excel(excel_path, sheet_name):
    exists = os.path.exists(excel_path)
    df = pd.DataFrame()
    detalle = ""
    try:
        if exists:
            df = pd.read_excel(excel_path, sheet_name=sheet_name, engine='openpyxl')
            return True, df, "Archivo Excel leído correctamente"
    except Exception as e:
        tb = traceback.extract_stack()
        detalle = f"{str(e)} \n {tb}"
    return False, df, f"No se puede leer la hoja {sheet_name} en el archivo {excel_path} \n{detalle}"


def check_string_in_df(df: pd.DataFrame, columns: list):
    try:
        for column in columns:
            df[column] = [str(v).strip() for v in df[column]]
        return True, df, f"Todas los valores han sido validados"
    except Exception as e:
        return False, df, f"No es posible realizar esta operación: {str(e)}"


def check_int_in_df(df: pd.DataFrame, columns: list):
    try:
        for column in columns:
            df[column] = [int(v) for v in df[column]]
        return True, f"Todas los valores han sido validados"
    except Exception as e:
        return False, f"No es posible realizar esta operación: {str(e)}"


def check_float_in_df(df: pd.DataFrame, columns: list):
    try:
        for column in columns:
            df[column] = [float(v) for v in df[column]]
        return True, df, f"Todas los valores han sido validados"
    except Exception as e:
        return False, df, f"No es posible realizar esta operación: {str(e)}"


def create_temporal_excel_from_args(args, temp_path):
    if args['excel_file'].mimetype in 'application/xls, application/vnd.ms-excel,  application/xlsx' \
                                      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        excel_file = args['excel_file']
        filename = excel_file.filename
        stream_excel_file = excel_file.stream.read()
        # path del archivo temporal a guardar para poderlo leer inmediatamente
        temp_file = os.path.join(temp_path, f"{str(randint(0, 100))}_{filename}")
        with open(temp_file, 'wb') as f:
            f.write(stream_excel_file)
        return os.path.exists(temp_file), temp_file, stream_excel_file
    else:
        return False, None, None
