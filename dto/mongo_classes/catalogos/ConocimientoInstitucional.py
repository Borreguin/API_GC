import uuid
from dto.mongo_classes import *


class ConocimientoInstitucional(Document):
    public_id = StringField(required=True, default=None, unique=True)
    idx = StringField(required=True, default=None, unique=True)
    conocimiento_institucional = StringField(required=True, unique=True)
    updated = DateTimeField(default=dt.datetime.now())
    document = StringField(required=True, default="ConocimientoInstitucional")
    meta = {"collection": "CATALOGO|ConocimientoInstitucional"}

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        if self.public_id is None:
            self.public_id = str(uuid.uuid4())

    def __repr__(self):
        return f"<C. Institucional {self.idx},{self.conocimiento_institucional}>"

    def __str__(self):
        return f"<C. Institucional {self.idx},{self.conocimiento_institucional}>"

    def to_dict(self):
        return dict(public_id=self.public_id, idx=self.idx,
                    conocimiento_institucional=self.conocimiento_institucional,
                    updated=self.updated.strftime(init.DEFAULT_DATE_FORMAT),
                    document=self.document)