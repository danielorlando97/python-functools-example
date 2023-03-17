from functools import singledispatchmethod
from typing import Protocol
from src.command_lines.command_lines import CommandLine, Student, Presence
from src.persistence.models import Model, StudentModel, PresenceModel
from src.errors import InformationError

class PersistenceLayerProtocol(Protocol):

    def create(self, model: Model):
        """
        It should persist a new instance in the persistence layer with the body
        It should also check if the body structure is correct
        """


class CommandLineHandlers:
    """
    This class implement the visitor pattern to control each command request.
    So, this class has a method for each system's command. 
    """

    def __init__(self, db: PersistenceLayerProtocol) -> None:
        self.db = db

    @singledispatchmethod
    def exec_cmd(self, cmd: CommandLine):
        """
        This is the main method of this class, it's decorated with singledispatchmethod,
        So, when this function is called it will analyze the type of cmd to call 
        the handler for that type.

        Each handler should take the sended information, transform it and save it 
        by the persistence layer
        """

    @exec_cmd.register
    def _(self, cmd: Student):
        self.db.create(StudentModel(name=cmd.name))

    @exec_cmd.register
    def _(self, cmd: Presence):
        h, m = cmd.start_time.split(':')
        # This function because the test said that the time is by 24 hours
        start_min = int(h) * 60 + int(m)

        h, m = cmd.end_time.split(':')
        # This function because the test said that the time is by 24 hours
        end_min = int(h) * 60 + int(m)

        if end_min <= start_min:
            raise InformationError("The start time can't be greater or equal than the end time")

        self.db.create(
            PresenceModel(
                name=cmd.student_name,
                day=cmd.day,
                start_time=cmd.start_time,
                start_min=start_min,
                end_time=cmd.end_time,
                end_min=end_min,
                delta_time=end_min - start_min,
                room=cmd.room
            )
        )
