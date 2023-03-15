from unittest import TestCase
from src.command_lines import Student, Presence
from src.command_line_handlers import CommandLineHandlers, PersistenceLayerProtocol, PersistenceRepositoryProtocol


class MockRepository(PersistenceRepositoryProtocol):
    def __init__(self) -> None:
        self.db = []

    def create(self, *arg, **kwds):
        self.db.append(kwds)


class MockPersistenceLayer(PersistenceLayerProtocol):

    def __getitem__(self, collection) -> PersistenceRepositoryProtocol:
        self.function_called = collection
        self.repo = MockRepository()
        return self.repo


class CommandHandlerTest(TestCase):
    def test_success_student_handling(self):

        db = MockPersistenceLayer()
        handler = CommandLineHandlers(db)
        student = Student('Daniel')

        handler.exec_cmd(student)

        assert db.function_called == 'Student'
        assert len(db.repo.db) == 1
        assert db.repo.db[0]['name'] == 'Daniel'

    def test_success_presence_handling(self):

        db = MockPersistenceLayer()
        handler = CommandLineHandlers(db)
        presence = Presence('Daniel', 1, '02:20', '10:40', 'F100')

        handler.exec_cmd(presence)

        assert db.function_called == 'Presence'
        assert len(db.repo.db) == 1
        assert db.repo.db[0]['name'] == 'Daniel'
        assert db.repo.db[0]['day'] == 1
        assert db.repo.db[0]['start_time'] == '02:20'
        assert db.repo.db[0]['end_time'] == '10:40'
        assert db.repo.db[0]['room'] == 'F100'

        start_min = 2 * 60 + 20
        end_min = 10 * 60 + 40

        assert db.repo.db[0]['start_min'] == start_min
        assert db.repo.db[0]['end_min'] == end_min

        assert db.repo.db[0]['delta_time'] == end_min - start_min
