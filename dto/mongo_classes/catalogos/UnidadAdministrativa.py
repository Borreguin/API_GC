import uuid
from dto.mongo_classes import *


class UnidadAdministrativa(Document):
    public_id = StringField(required=True, default=None, unique=True)
    idx = StringField(required=True, default=None, unique=True)
    cod_unidad_administrativa = StringField(required=True, unique=True)
    nombre = StringField(required=True, unique=True)
    updated = DateTimeField(default=dt.datetime.now())
    document = StringField(required=True, default="UnidadAdministrativa")
    meta = {"collection": "CATALOGO|UnidadAdministrativa"}

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        if self.public_id is None:
            self.public_id = str(uuid.uuid4())

    def __repr__(self):
        return f"<UnidadAdministrativa {self.cod_unidad_administrativa}, {self.nombre}>"

    def __str__(self):
        return f"<UnidadAdministrativa {self.cod_unidad_administrativa}, {self.nombre}>"

    def to_dict(self):
        return dict(public_id=self.public_id, idx=self.idx,
                    cod_unidad_administrativa=self.cod_unidad_administrativa,
                    updated=self.updated.strftime(init.DEFAULT_DATE_FORMAT),
                    document=self.document)
