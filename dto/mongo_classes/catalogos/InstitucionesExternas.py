import uuid
from dto.mongo_classes import *


class InstitucionesExternas(Document):
    public_id = StringField(required=True, default=None, unique=True)
    id = StringField(required=True, default=None, unique=True)
    codigo = StringField(required=True, unique=True)
    nombre = StringField(required=True, unique=True)
    updated = DateTimeField(default=dt.datetime.now())
    document = StringField(required=True, default="InstitucionesExternas")
    meta = {"collection": "CATALOGO|InstitucionesExternas"}

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        if self.public_id is None:
            self.public_id = str(uuid.uuid4())

    def __repr__(self):
        return f"<InstitucionesExternas {self.codigo},{self.nombre}>"

    def __str__(self):
        return f"<InstitucionesExternas {self.codigo},{self.nombre}>"

    def to_dict(self):
        return dict(public_id=self.public_id, id=self.id,
                    nombre=self.nombre,
                    updated=self.updated.strftime(init.DEFAULT_DATE_FORMAT),
                    document=self.document)