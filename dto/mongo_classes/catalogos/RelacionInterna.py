import uuid
from dto.mongo_classes import *
from my_lib.utils import create_excel_file_from_dicts


class RelacionInterna(Document):
    public_id = StringField(required=True, default=None, unique=True)
    idx = StringField(required=True, default=None, unique=True)
    codigo = StringField(required=True, unique=True)
    nombre = StringField(required=True, unique=True)
    updated = DateTimeField(default=dt.datetime.now())
    document = StringField(required=True, default="RelacionInterna")
    meta = {"collection": "CATALOGO|RelacionInterna"}

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        if self.public_id is None:
            self.public_id = str(uuid.uuid4())

    def __repr__(self):
        return f"<RelacionInterna {self.codigo},{self.nombre}>"

    def __str__(self):
        return f"<RelacionInterna {self.codigo},{self.nombre}>"

    def to_dict(self):
        return dict(public_id=self.public_id, idx=self.idx, codigo=self.codigo, nombre=self.nombre,
                    updated=self.updated.strftime(init.DEFAULT_DATE_FORMAT),
                    document=self.document)

    def to_update(self):
        return dict(idx=self.idx, nombre=self.nombre, codigo=self.codigo,
                    updated=self.updated.strftime(init.DEFAULT_DATE_FORMAT),
                    document=self.document)


class RelacionInternaAsDataFrame:
    def __init__(self, excel_path=None):
        """
        This class allows to get RelacionInterna's DataFrame from Excel or Mongo DataBase
        :param excel_path: If one gets a dataFrame from excel
        """
        self.excel_path = excel_path
        self.sheet_name = "relaciones_internas"
        # columns for this DataFrame
        self.cl_id = "idx"
        self.cl_codigo = "codigo"
        self.cl_nombre = "nombre"
        self.df = pd.DataFrame()
        # columns to check in the excel file
        self.main_columns = [self.cl_id, self.cl_codigo, self.cl_nombre]
        self.has_valid_df = False

    def validate(self):
        # read excel file and verify if this excel file is correct
        success, df, msg = u.get_df_from_excel(self.excel_path, self.sheet_name)
        if not success:
            return False, msg
        self.df = df

        # lower and strip all the names of the columns
        self.df.columns = [str(x).lower().strip() for x in df.columns]
        # check if all columns are present
        check = [(str(c) in self.df.columns) for c in self.main_columns]
        # incorrect format:
        if not all(check):
            to_send = [self.main_columns[i] for i, v in enumerate(check) if not v]
            return False, f"La hoja {self.sheet_name} no contiene los campos: {to_send}. " \
                          f"Los campos necesarios son: [{str(self.main_columns)}]"

        # selecting only the desired columns
        self.df = self.df[self.main_columns]
        self.df = self.df.dropna()
        self.df = self.df.drop_duplicates([self.cl_id])

        if self.df.empty:
            return False, f"La hoja {self.sheet_name} se encuentra vacía"

        success, self.df, msg = u.check_string_in_df(self.df, [self.cl_id, self.cl_codigo])
        if not success:
            return False, msg
        # if all is correct then:
        self.has_valid_df = True
        return True, f"Hoja {self.sheet_name} validada correctamente"

    def get_object_list_from_excel(self):
        # gets a list of RelacionInterna's objects
        if not self.has_valid_df:
            # validate the excel file as DataFrame
            success, msg = self.validate()
            # if is a valid DataFrame then repeat this function
            if success:
                return self.get_object_list_from_excel()
            # else nothing to do
            return False, list(), msg
        try:
            lst = list()
            for idx in self.df.index:
                param = dict(self.df.iloc[idx])
                item = RelacionInterna(**param)
                lst.append(item)
            return True, lst, "Lista de objetos creada de manera correcta"
        except Exception as e:
            return False, list(), f"Ha ocurrido un error al generar los objectos tipo RelacionInterna: {str(e)}"

    def get_excel_from_db(self, path_file: str, columns: list = None):
        items_as_dict = [it.to_dict() for it in RelacionInterna.objects.all()]
        if len(items_as_dict) == 0:
            return False, "No existen registros asociados"
        columns = self.main_columns if columns is None else columns
        return create_excel_file_from_dicts(path_file, self.sheet_name, items_as_dict, columns)