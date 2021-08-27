from sqlalchemy import create_engine
import settings.initial_settings as init
import pandas as pd

from my_lib.SQLHandler.Statements import persona_table, info_personal_basica, asp_net_user_basic_info, \
    funcionarios_info_basica
import my_lib.SQLHandler.Keys as Keys


class SQLGestionConocimiento:

    def __init__(self, default_db="", port=1433):
        self.server_name = init.GCAPP_SERVER_NAME
        self.port = port
        self.default_db = default_db
        self.user = init.GCAPP_USER
        self.password = init.GCAPP_PASSWORD
        self.engine = self.set_engine()

    def set_engine(self):
        return create_engine(
            f"mssql+pymssql://{self.user}:{self.password}@{self.server_name}:{self.port}/{self.default_db}")

    def execute_as_dataframe(self, sql_statement: str) -> (bool, pd.DataFrame, str):
        try:
            df_result = pd.read_sql(sql_statement, self.engine)
            return True, pd.DataFrame(df_result), "Petición éxitosa"
        except Exception as e:
            msg = f"No se ha ejecutado correctamente [{sql_statement}] \n{str(e)}"
            return False, pd.DataFrame(), msg

    def get_users(self):
        # Get basic information:
        success_1, df_funcionarios_info, msg_1 = self.get_funcionarios()
        success_2, df_net_user, msg_2 = self.execute_as_dataframe(asp_net_user_basic_info)
        if not success_1 or not success_2:
            return False, pd.DataFrame(), msg_1 if not success_1 else msg_2
        # Processing information:
        df_net_user.rename(columns={"Id": Keys.per_user_id}, inplace=True)
        df_merge = pd.merge(df_net_user, df_funcionarios_info, on=Keys.per_user_id, how="left")
        # df_merge.dropna(subset=[Keys.per_user_id], inplace=True)
        return True, df_merge, "Información usuarios OK"

    def get_funcionarios(self):
        success, df_funcionarios_info, msg = self.execute_as_dataframe(funcionarios_info_basica)
        df_funcionarios_info[Keys.per_user_id] = [str(u) for u in df_funcionarios_info[Keys.per_user_id]]
        df_result = pd.DataFrame(columns=list(df_funcionarios_info.columns) +
                                         [Keys.telCelular, Keys.telDomicilio, Keys.telTrabajo])
        df_funcionarios_info.set_index(keys=[Keys.per_id], inplace=True)
        for idx, _df in df_funcionarios_info.groupby(by=[Keys.fun_numero_documento,
                                                         Keys.tiptel_tipo, Keys.tel_numero]):
            fun_numero_documento, tiptel_tipo, tel_numero = idx
            per_id = _df.index[0]
            if len(_df.index) > 1:
                _df.iloc[0][Keys.co_correo] = "; ".join(list(_df[Keys.co_correo]))
                _df = _df.iloc[0]

            # existe este registro actualmente:
            if per_id not in df_result.index:
                # no existe, crear un nuevo registro
                df = _df
            else:
                # ya existe, actualizar
                df = df_result.loc[per_id]

            if tiptel_tipo == "Celular":
                df[Keys.telCelular] = tel_numero
            if tiptel_tipo == "Convencional":
                df[Keys.telDomicilio] = tel_numero
            if tiptel_tipo == "Trabajo":
                df[Keys.telTrabajo] = tel_numero

            # existe este registro actualmente:
            if per_id not in df_result.index:
                df_result = df_result.append(_df)
            else:
                df_result.loc[per_id] = df
        df_result[Keys.telExtension] = df_result[Keys.tel_extension]
        to_remove = [Keys.tel_extension, Keys.tel_numero, Keys.tiptel_tipo]
        df_result.drop(labels=to_remove, axis=1, inplace=True)
        df_result[Keys.per_id] = list(df_result.index)
        df_result[Keys.per_user_id] = [str(u) for u in df_result[Keys.per_user_id]]
        return True, df_result, "Tabla funcionarios ok"


def test_connection():
    gcServer = SQLGestionConocimiento()
    sql_statement = "SELECT * FROM [GESTION_CONOCIMIENTO].[dbo].[INFORMACION_PERSONAL_BASICA]"
    df_prueba = pd.read_sql(sql_statement, gcServer.engine)
    print(df_prueba)


if __name__ == "__main__":
    if init.DEBUG:
        test_connection()
