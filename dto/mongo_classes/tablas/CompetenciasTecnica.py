import uuid
from dto.mongo_classes import *


class CompetenciasTecnica(Document):
    public_id = StringField(required=True, default=None, unique=True)
    id = StringField(required=True, default=None, unique=True)
    denominacion_competencia = StringField(required=True, default="")
    definicion = StringField(required=True, default="")
    item = IntField(required=True, default=0)
    nivel = StringField(required=True, default="Bajo", choices=["Alto", "Medio", "Bajo"])
    comportamiento_observable = StringField(required=True, default="")
    updated = DateTimeField(default=dt.datetime.now())
    document = StringField(required=True, default="CompetenciasTecnica")
    meta = {"collection": "TABLA|CompetenciasTecnica"}

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        if self.public_id is None:
            self.public_id = str(uuid.uuid4())

    def __repr__(self):
        return f"<CompetenciasTecnica {self.id}, {self.denominacion_competencia}, {self.item}, {self.nivel}>"

    def __str__(self):
        return f"<CompetenciasTecnica {self.id}, {self.denominacion_competencia}, {self.item}, {self.nivel}>"

    def to_dict(self):
        return dict(public_id=self.public_id, id=self.id,
                    denominacion_competencia=self.denominacion_competencia, definicion=self.definicion, item=self.item,
                    nivel=self.nivel, comportamiento_observable=self.comportamiento_observable,
                    updated=self.updated.strftime(init.DEFAULT_DATE_FORMAT),
                    document=self.document)