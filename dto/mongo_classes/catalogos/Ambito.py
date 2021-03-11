import uuid
from dto.mongo_classes import *


class Ambito(Document):
    public_id = StringField(required=True, default=None, unique=True)
    idx = StringField(required=True, default=None, unique=True)
    ambito = StringField(required=True, unique=True)
    updated = DateTimeField(default=dt.datetime.now())
    document = StringField(required=True, default="Ambito")
    meta = {"collection": "CATALOGO|Ambito"}

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        if self.public_id is None:
            self.public_id = str(uuid.uuid4())

    def __repr__(self):
        return f"<Ambito{self.idx},{self.ambito}>"

    def __str__(self):
        return f"<Ambito {self.idx},{self.ambito}>"

    def to_dict(self):
        return dict(public_id=self.public_id, idx=self.idx,
                    ambito=self.ambito,
                    updated=self.updated.strftime(init.DEFAULT_DATE_FORMAT),
                    document=self.document)


class AmbitoFromDataFrame:
    def __init__(self, excel_path):
        self.excel_path = excel_path
        self.sheet_name = "catalogo_ambito"
        # columns for this DataFrame
        self.cl_id = "idx"
        self.cl_ambito = "ambito"
        self.df = pd.DataFrame()
        # columns to check in the excel file
        self.check_columns = [self.cl_id, self.cl_ambito]
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
        check = [(str(c) in self.df.columns) for c in self.check_columns]
        # incorrect format:
        if not all(check):
            to_send = [self.check_columns[i] for i, v in enumerate(check) if not v]
            return False, f"La hoja {self.sheet_name} no contiene los campos: {to_send}. " \
                          f"Los campos necesarios son: [{str(self.check_columns)}]"

        # selecting only the desired columns
        self.df = self.df[self.check_columns]

        if self.df.empty:
            return False, f"La hoja {self.sheet_name} se encuentra vacía"

        success, self.df, msg = u.check_string_in_df(self.df, [self.cl_id, self.cl_ambito])
        if not success:
            return False, msg
        # if all is correct then:
        self.has_valid_df = True
        return True, f"Hoja {self.sheet_name} validada correctamente"

    def get_list(self):
        # gets a list of Ambito's objects
        if not self.has_valid_df:
            # validate the excel file as DataFrame
            success, msg = self.validate()
            # if is a valid DataFrame then repeat this function
            if success:
                return self.get_list()
            # else nothing to do
            return False, list(), msg
        try:
            lst = list()
            for idx in self.df.index:
                param = dict(self.df.iloc[idx])
                item = Ambito(**param)
                lst.append(item)
            return True, lst, "Lista de objetos creada de manera correcta"
        except Exception as e:
            return False, list(), f"Ha ocurrido un error al generar los objectos tipo Ambito: {str(e)}"