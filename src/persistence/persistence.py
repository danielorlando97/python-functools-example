from src.command_lines.command_line_handlers import PersistenceLayerProtocol
from typing import Dict, List
from collections import defaultdict
from functools import singledispatchmethod
from src.persistence.models import Model, StudentModel, PresenceModel
from src.use_cases.scholar_time_by_students import PersistenceScholarTimeProtocol

class MemoryPersistenceLayer(
    PersistenceLayerProtocol,
    PersistenceScholarTimeProtocol
):
    
    def __init__(self) -> None:
        self.db : Dict[str, Dict[int, List]] = {}

    @singledispatchmethod
    def create(self, model: Model):
        """"""
    
    @create.register
    def _(self, model: StudentModel):
        self.db[model.name] = defaultdict(list)

    @create.register
    def _(self, model: PresenceModel):
        try:
            collection = self.db[model.name]
        except KeyError:
            raise Exception("Unknown Student")

        collection[model.day].append(model)

    def student_names(self):
        return self.db.keys()
    
    def student_presence_group_by_day(self, student_name) -> Dict[int, List]:
        return self.db[student_name]
