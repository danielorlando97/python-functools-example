from functools import singledispatchmethod
from typing import Protocol
from src.command_lines import CommandLine, Student, Presence


class PersistenceRepositoryProtocol(Protocol):
    def create(self, **body):
        """
        It should persist a new instance in the persistence layer with the body
        It should also check if the body structure is correct
        """


class PersistenceLayerProtocol(Protocol):

    def __getitem__(self, collection) -> PersistenceRepositoryProtocol:
        """It should return the repository for that collection"""


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
        self.db['Student'].create(name=cmd.name)

    @exec_cmd.register
    def _(self, cmd: Presence):
        h, m = cmd.start_time.split(':')
        # This function because the test said that the time is by 24 hours
        start_min = int(h) * 60 + int(m)

        h, m = cmd.end_time.split(':')
        # This function because the test said that the time is by 24 hours
        end_min = int(h) * 60 + int(m)

        self.db['Presence'].create(
            name=cmd.student_name,
            day=cmd.day,
            start_time=cmd.start_time,
            start_min=start_min,
            end_time=cmd.end_time,
            end_min=end_min,
            delta_time=end_min - start_min,
            room=cmd.room
        )
