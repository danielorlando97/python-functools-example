from src.command_lines.command_line_handlers import PersistenceLayerProtocol
from typing import Dict, List, Set
from collections import defaultdict
from functools import singledispatchmethod
from src.persistence.models import Model, StudentModel, PresenceModel, ClassroomModel
from src.use_cases.scholar_time_by_students import PersistenceScholarTimeProtocol
from src.errors import PersistenceError

class MemoryPersistenceLayer(
    PersistenceLayerProtocol,
    PersistenceScholarTimeProtocol
):
    
    def __init__(self) -> None:
        self.db : Dict[str, Dict[int, List]] = {}
        self.rooms: Dict[str, ClassroomModel] = {}

    @singledispatchmethod
    def create(self, model: Model):
        """It should save each model in the memory db"""
    
    @create.register
    def _(self, model: StudentModel):
        self.db[model.name] = defaultdict(list)

    @create.register
    def _(self, model: PresenceModel):
        try:
            collection = self.db[model.name]
        except KeyError:
            raise PersistenceError("Unknown Student")

        try:
            _ = self.rooms[model.room]
        except KeyError:
            raise PersistenceError("Unknown Classroom")

        collection[model.day].append(model)

    @create.register
    def _(self, model: ClassroomModel):
        self.rooms[model.room_code] = model
    

    def student_names(self):
        return self.db.keys()
    
    def student_presence_group_by_day(self, student_name) -> Dict[int, List]:
        try:
            return self.db[student_name]
        except KeyError:
            raise PersistenceError("Unknown Student")
    
    def student_presence_group_by_day_and_classrooms(self, student_name, *rooms) -> Dict[int, List]:
        result = {}
        for day, presences in self.student_presence_group_by_day(student_name).items():
            new_presences = [x for x in presences if x.room in rooms]
            if new_presences:
                result[day] = new_presences
            
        return result
    
    def room_codes_in_building(self, building) -> List[str]:
        return [x for x in self.rooms if x.building == building]


    