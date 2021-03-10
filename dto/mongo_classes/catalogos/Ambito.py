import uuid
from dto.mongo_classes import *


class Ambito(Document):
    public_id = StringField(required=True, default=None, unique=True)
    id = StringField(required=True, default=None, unique=True)
    ambito = StringField(required=True, unique=True)
    updated = DateTimeField(default=dt.datetime.now())
    document = StringField(required=True, default="Ambito")
    meta = {"collection": "CATALOGO|Ambito"}

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        if self.public_id is None:
            self.public_id = str(uuid.uuid4())

    def __repr__(self):
        return f"<Ambito{self.id},{self.ambito}>"

    def __str__(self):
        return f"<Ambito {self.id},{self.ambito}>"

    def to_dict(self):
        return dict(public_id=self.public_id, id=self.id,
                    ambito=self.ambito,
                    updated=self.updated.strftime(init.DEFAULT_DATE_FORMAT),
                    document=self.document)