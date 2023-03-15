from unittest import TestCase
from src.command_lines.command_lines import Student, Presence
from src.command_lines.command_line_handlers import CommandLineHandlers, PersistenceLayerProtocol
from src.persistence.models import StudentModel, PresenceModel
from collections import defaultdict
class MockRepository(PersistenceLayerProtocol):
    def __init__(self) -> None:
        self.db = {}

    def create(self, model):
        if isinstance(model, StudentModel):
            self.db[model.name] = defaultdict(list)
            self.function_called = 'Student'
        if isinstance(model, PresenceModel):
            self.db[model.name][model.day] = model
            self.function_called = 'Presence'

class CommandHandlerTest(TestCase):

    def test_success_student_handling(self):

        db = MockRepository()
        handler = CommandLineHandlers(db)
        student = Student('Daniel')

        handler.exec_cmd(student)

        assert db.function_called == 'Student'
        assert len(db.db) == 1
        assert 'Daniel' in db.db

    def test_success_presence_handling(self):

        db = MockRepository()
        db.create(StudentModel("Daniel"))
        handler = CommandLineHandlers(db)
        presence = Presence('Daniel', 1, '02:20', '10:40', 'F100')

        handler.exec_cmd(presence)

        assert db.function_called == 'Presence'
        assert 1 in db.db['Daniel']

        start_min = 2 * 60 + 20
        end_min = 10 * 60 + 40

        assert db.db['Daniel'][1].start_min == start_min
        assert db.db['Daniel'][1].end_min == end_min
        assert db.db['Daniel'][1].delta_time == end_min - start_min