import uuid
from dto.mongo_classes import *


class Mision(Document):
    public_id = StringField(required=True, default=None, unique=True)
    idx = StringField(required=True, default=None, unique=True)
    nombre = StringField(required=True, unique=True)
    descripcion = StringField(required=True)
    updated = DateTimeField(default=dt.datetime.now())
    document = StringField(required=True, default="Mision")
    meta = {"collection": "CATALOGO|Mision"}

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        if self.public_id is None:
            self.public_id = str(uuid.uuid4())

    def __repr__(self):
        return f"<Mision {self.nombre}, {self.descripcion}>"

    def __str__(self):
        return f"<Mision {self.nombre}, {self.descripcion}>"

    def to_dict(self):
        return dict(public_id=self.public_id, idx=self.idx,
                    nombre=self.nombre, descripcion=self.descripcion,
                    updated=self.updated.strftime(init.DEFAULT_DATE_FORMAT),
                    document=self.document)