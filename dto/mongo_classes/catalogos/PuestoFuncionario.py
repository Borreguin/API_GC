import uuid
from dto.mongo_classes import *


class PuestoFuncionario(Document):
    public_id = StringField(required=True, default=None, unique=True)
    id = StringField(required=True, default=None, unique=True)
    puesto_nombre = StringField(required=True, unique=True)
    updated = DateTimeField(default=dt.datetime.now())
    document = StringField(required=True, default="PuestoFuncionario")
    meta = {"collection": "CATALOGO|PuestoFuncionario"}

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        if self.public_id is None:
            self.public_id = str(uuid.uuid4())

    def __repr__(self):
        return f"<Funcionario {self.id}, {self.puesto_nombre}>"

    def __str__(self):
        return f"<Funcionario {self.id}, {self.puesto_nombre}>"

    def to_dict(self):
        return dict(public_id=self.public_id, id_nombre=self.id,
                    puesto_nombre=self.puesto_nombre, updated=self.updated.strftime(init.DEFAULT_DATE_FORMAT),
                    document=self.document)
