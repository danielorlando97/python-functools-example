from dataclasses import dataclass

class Model:
    """Root of class """

@dataclass
class StudentModel(Model):
    name: str

@dataclass
class PresenceModel(Model):
    name : str
    day : int
    start_time : str
    start_min : int
    end_time : str
    end_min : int
    delta_time : int
    room : str

    # def __eq__(self, __o: object) -> bool:
    #     if isinstance(__o, PresenceModel):
    #         return (
    #             __o.name == self.name and
    #             __o.day == self.day and
    #             __o.start_min == self.start_min and
    #             __o.delta_time == self.delta_time
    #         ) 
        
    #     return False