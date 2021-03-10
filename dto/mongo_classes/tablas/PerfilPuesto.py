import uuid
from dto.mongo_classes import *


class PerfilPuesto(Document):
    public_id = StringField(required=True, default=None, unique=True)
    id = StringField(required=True, default=None, unique=True)
    nivel = StringField(required=True, default="")
    rol = StringField(required=True, default="")
    grupo_ocupacional = StringField(required=True)
    grado = IntField(required=True, default=0)
    instruccion_formal = StringField(required=True, default="")
    experiencia = StringField(required=True, default="No requerida")
    updated = DateTimeField(default=dt.datetime.now())
    document = StringField(required=True, default="PerfilPuesto")
    meta = {"collection": "TABLA|PerfilPuesto"}

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        if self.public_id is None:
            self.public_id = str(uuid.uuid4())

    def __repr__(self):
        return f"<PerfilPuesto {self.id}, {self.grupo_ocupacional}, {self.instruccion_formal}>"

    def __str__(self):
        return f"<PerfilPuesto {self.id}, {self.grupo_ocupacional}, {self.instruccion_formal}>"

    def to_dict(self):
        return dict(public_id=self.public_id, id=self.id, nivel=self.nivel, rol=self.rol,
                    grupo_ocupacional=self.grupo_ocupacional, grado=self.grado,
                    instruccion_formal=self.instruccion_formal, experiencia=self.experiencia,
                    updated=self.updated.strftime(init.DEFAULT_DATE_FORMAT),
                    document=self.document)